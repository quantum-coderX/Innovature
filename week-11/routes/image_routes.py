"""
image_routes.py  –  Week 10
============================
REST endpoints for product image upload, listing, deletion, and primary-flag.

Endpoints
---------
POST   /api/products/<id>/images            Upload 1-N images (multipart/form-data)
GET    /api/products/<id>/images            List all images for a product
DELETE /api/products/<id>/images/<img_id>  Delete one image + its thumbnail from disk
PATCH  /api/products/<id>/images/<img_id>/primary  Set as the product's cover photo
"""

import os

from flask import Blueprint, request, current_app

from database import db
from models import Product, ProductImage
from serializers import (
    serialize_product_image,
    serialize_product_images,
    error_response,
    success_response,
)
from auth import seller_required, jwt_required_active_user, get_current_user
from image_utils import save_product_image

image_bp = Blueprint("images", __name__, url_prefix="/api/products")


# ─────────────────────────────────────────────────────────────────────────────
# POST  /api/products/<product_id>/images
# Upload one or more images for a product (multipart/form-data, key = "images")
# ─────────────────────────────────────────────────────────────────────────────

@image_bp.route("/<int:product_id>/images", methods=["POST"])
@seller_required
def upload_images(product_id):
    """
    Upload product images.

    • Multipart/form-data, field name: images  (can repeat for multiple files)
    • Max 5 images total per product (existing + new)
    • Validates MIME type (jpeg/png/webp) and size (≤5 MB) per file
    • Saves originals to  static/uploads/products/
    • Generates 300×300 thumbnails in  static/uploads/thumbnails/
    • First image uploaded becomes primary if product has no images yet
    """
    current_user = get_current_user()

    # ── 1. Verify product exists and belongs to caller ─────────
    product = db.session.get(Product, product_id)
    if not product:
        return error_response("Product not found", 404)
    if product.seller_id != current_user.id:
        return error_response("Forbidden: you can only upload images to your own products", 403)

    # ── 2. Check incoming files ─────────────────────────────────
    files = request.files.getlist("images")
    if not files or all(f.filename == "" for f in files):
        return error_response("No files provided. Use field name 'images' in form-data")

    # ── 3. Enforce max-images-per-product cap ───────────────────
    max_images: int = current_app.config["MAX_IMAGES_PER_PRODUCT"]
    existing_count = ProductImage.query.filter_by(product_id=product_id).count()
    slots_left = max_images - existing_count

    valid_files = [f for f in files if f.filename]
    if len(valid_files) > slots_left:
        return error_response(
            f"Upload rejected: product already has {existing_count} image(s). "
            f"Maximum is {max_images}. You can upload at most {slots_left} more."
        )

    # ── 4. Process each file ────────────────────────────────────
    uploaded = []
    errors = []

    for file in valid_files:
        try:
            meta = save_product_image(file)
        except ValueError as exc:
            errors.append({"filename": file.filename, "error": str(exc)})
            continue

        # Determine is_primary: true only for the first ever image
        is_primary = (existing_count == 0 and len(uploaded) == 0)

        img = ProductImage(
            product_id=product_id,
            filename=meta["filename"],
            thumbnail=meta["thumbnail"],
            image_url=meta["image_url"],
            thumbnail_url=meta["thumbnail_url"],
            file_size=meta["file_size"],
            mime_type=meta["mime_type"],
            is_primary=is_primary,
        )
        db.session.add(img)
        db.session.flush()   # get img.id before commit
        uploaded.append(img)

    if not uploaded and errors:
        # Every file failed validation — roll back and report
        db.session.rollback()
        return {
            "error": "All files failed validation",
            "details": errors,
        }, 400

    db.session.commit()

    response_data = {
        "uploaded": serialize_product_images(uploaded),
        "errors":   errors,
        "total_images": ProductImage.query.filter_by(product_id=product_id).count(),
    }
    msg = f"{len(uploaded)} image(s) uploaded successfully"
    if errors:
        msg += f"; {len(errors)} file(s) rejected"

    return success_response(response_data, msg, 201)


# ─────────────────────────────────────────────────────────────────────────────
# GET  /api/products/<product_id>/images
# Public – list all images for a product
# ─────────────────────────────────────────────────────────────────────────────

@image_bp.route("/<int:product_id>/images", methods=["GET"])
def list_images(product_id):
    """Return all images for a product, primary first."""
    product = db.session.get(Product, product_id)
    if not product:
        return error_response("Product not found", 404)

    images = (
        ProductImage.query
        .filter_by(product_id=product_id)
        .order_by(ProductImage.is_primary.desc(), ProductImage.created_at.asc())
        .all()
    )

    return success_response({
        "product_id":   product_id,
        "product_name": product.name,
        "count":        len(images),
        "images":       serialize_product_images(images),
    })


# ─────────────────────────────────────────────────────────────────────────────
# DELETE  /api/products/<product_id>/images/<image_id>
# Remove one image and its thumbnail from disk + database
# ─────────────────────────────────────────────────────────────────────────────

@image_bp.route("/<int:product_id>/images/<int:image_id>", methods=["DELETE"])
@seller_required
def delete_image(product_id, image_id):
    """
    Delete a product image.

    If the deleted image was the primary, the next oldest image is
    automatically promoted to primary.
    """
    current_user = get_current_user()

    product = db.session.get(Product, product_id)
    if not product:
        return error_response("Product not found", 404)
    if product.seller_id != current_user.id:
        return error_response("Forbidden: you can only delete images from your own products", 403)

    image = ProductImage.query.filter_by(id=image_id, product_id=product_id).first()
    if not image:
        return error_response("Image not found", 404)

    was_primary = image.is_primary

    # ── Remove files from disk ──────────────────────────────────
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    thumb_folder  = current_app.config["THUMBNAIL_FOLDER"]

    _try_delete(os.path.join(upload_folder, image.filename))
    _try_delete(os.path.join(thumb_folder, image.thumbnail))

    db.session.delete(image)
    db.session.flush()

    # ── Auto-promote next image to primary if needed ────────────
    if was_primary:
        next_image = (
            ProductImage.query
            .filter_by(product_id=product_id)
            .order_by(ProductImage.created_at.asc())
            .first()
        )
        if next_image:
            next_image.is_primary = True

    db.session.commit()
    return success_response(None, "Image deleted successfully")


# ─────────────────────────────────────────────────────────────────────────────
# PATCH  /api/products/<product_id>/images/<image_id>/primary
# Set an image as the product's cover / primary photo
# ─────────────────────────────────────────────────────────────────────────────

@image_bp.route("/<int:product_id>/images/<int:image_id>/primary", methods=["PATCH"])
@seller_required
def set_primary_image(product_id, image_id):
    """Mark the given image as the product's primary/cover photo."""
    current_user = get_current_user()

    product = db.session.get(Product, product_id)
    if not product:
        return error_response("Product not found", 404)
    if product.seller_id != current_user.id:
        return error_response("Forbidden", 403)

    target = ProductImage.query.filter_by(id=image_id, product_id=product_id).first()
    if not target:
        return error_response("Image not found", 404)

    # Clear existing primary flag
    ProductImage.query.filter_by(product_id=product_id, is_primary=True).update(
        {"is_primary": False}
    )
    target.is_primary = True
    db.session.commit()

    return success_response(serialize_product_image(target), "Primary image updated")


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _try_delete(path: str) -> None:
    """Delete a file silently if it exists."""
    try:
        if os.path.isfile(path):
            os.remove(path)
    except OSError:
        pass  # log this in production; for now swallow
