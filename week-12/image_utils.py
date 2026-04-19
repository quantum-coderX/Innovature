"""
image_utils.py  –  Week 10
===========================
Utilities for:
  • Validating uploaded image files  (MIME type + file size)
  • Generating 300×300 thumbnails using Pillow
"""

import os
import uuid
import imghdr
from io import BytesIO

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image
from flask import current_app
from werkzeug.datastructures import FileStorage


# ─────────────────────────────────────────────────────────────────────────────
# MIME-type detection helpers
# ─────────────────────────────────────────────────────────────────────────────

# Mapping from imghdr return value → canonical MIME type
_IMGHDR_TO_MIME = {
    "jpeg": "image/jpeg",
    "png":  "image/png",
    "webp": "image/webp",
}

# Mapping from MIME type → save extension (always store as a compressed format)
MIME_TO_EXT = {
    "image/jpeg": "jpg",
    "image/png":  "png",
    "image/webp": "webp",
}


def _detect_mime(file_bytes: bytes) -> str | None:
    """
    Detect the actual image format from the raw bytes (magic-number based).
    Returns MIME string like 'image/jpeg', or None if unrecognised.
    """
    # imghdr reads the file header to determine format
    fmt = imghdr.what(None, h=file_bytes[:32])
    return _IMGHDR_TO_MIME.get(fmt)


# ─────────────────────────────────────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────────────────────────────────────

def validate_image(file: FileStorage) -> tuple[bool, str | None, str | None]:
    """
    Validate an uploaded image file.

    Returns:
        (ok, error_message, detected_mime_type)
        • ok=True  → file is valid; mime_type is set
        • ok=False → file is invalid; error_message explains why
    """
    allowed_types: set = current_app.config["ALLOWED_IMAGE_TYPES"]
    max_size: int = current_app.config["MAX_IMAGE_SIZE_BYTES"]

    # Read entire file into memory for size + magic-number check
    file.seek(0)
    file_bytes = file.read()
    file.seek(0)  # reset so caller can re-read if needed

    # ── 1. Size check ──────────────────────────────────────────
    size = len(file_bytes)
    if size == 0:
        return False, "File is empty", None
    if size > max_size:
        mb = max_size / (1024 * 1024)
        return False, f"File too large. Maximum allowed size is {mb:.0f} MB", None

    # ── 2. MIME / magic-number check ───────────────────────────
    mime = _detect_mime(file_bytes)
    if mime is None or mime not in allowed_types:
        allowed = ", ".join(sorted(allowed_types))
        return False, f"Invalid file type. Allowed types: {allowed}", None

    return True, None, mime


# ─────────────────────────────────────────────────────────────────────────────
# Filename helpers
# ─────────────────────────────────────────────────────────────────────────────

def _safe_stem(original_filename: str) -> str:
    """
    Strip directory components and extension from the original filename,
    keeping only URL-safe characters.
    """
    base = os.path.basename(original_filename or "image")
    stem, _ = os.path.splitext(base)
    # Replace anything non-alphanumeric with underscore
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in stem)
    return safe[:60] or "image"


def build_filenames(original_filename: str, mime: str) -> tuple[str, str]:
    """
    Build unique on-disk filenames for the original and thumbnail.

    Returns:
        (image_filename, thumbnail_filename)
        e.g. ("a1b2c3_photo.jpg", "thumb_a1b2c3_photo.jpg")
    """
    uid = uuid.uuid4().hex[:12]
    stem = _safe_stem(original_filename)
    ext = MIME_TO_EXT.get(mime, "jpg")
    fname = f"{uid}_{stem}.{ext}"
    thumb = f"thumb_{uid}_{stem}.jpg"   # thumbnails always saved as JPEG
    return fname, thumb


# ─────────────────────────────────────────────────────────────────────────────
# Thumbnail generation
# ─────────────────────────────────────────────────────────────────────────────

def generate_thumbnail_bytes(image_bytes: bytes, size: tuple = (300, 300)) -> bytes:
    """
    Create a thumbnail from raw image bytes and return thumbnail bytes.

    Algorithm:
      • Open the image with Pillow.
      • Convert RGBA / palette images → RGB so JPEG can be written.
      • thumbnail() resizes *in-place*, preserving aspect ratio, so the
        result fits within *size* without cropping.
      • Save as JPEG (quality=85) for consistent small file size.

    Args:
        image_bytes: Raw bytes of the original image.
        size:        Max (width, height) of the thumbnail (default 300×300).
    """
    img = Image.open(BytesIO(image_bytes))

    # Pillow's thumbnail() modifies img in-place and is aspect-ratio safe
    img.thumbnail(size, Image.LANCZOS)

    # Convert to RGB; required for JPEG (which has no alpha channel)
    if img.mode in ("RGBA", "P", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        background.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")

    out = BytesIO()
    img.save(out, "JPEG", quality=85, optimize=True)
    return out.getvalue()


def _get_storage_backend() -> str:
    return current_app.config.get("STORAGE_BACKEND", "local").lower()


def _build_s3_url(key: str) -> str:
    custom_domain = current_app.config.get("S3_CUSTOM_DOMAIN", "").strip()
    if custom_domain:
        return f"https://{custom_domain}/{key}"

    bucket = current_app.config.get("AWS_S3_BUCKET", "").strip()
    region = current_app.config.get("AWS_REGION", "us-east-1").strip() or "us-east-1"
    return f"https://{bucket}.s3.{region}.amazonaws.com/{key}"


def _s3_client():
    kwargs = {
        "region_name": current_app.config.get("AWS_REGION", "us-east-1"),
    }
    endpoint_url = current_app.config.get("AWS_S3_ENDPOINT_URL", "").strip()
    access_key = current_app.config.get("AWS_ACCESS_KEY_ID", "").strip()
    secret_key = current_app.config.get("AWS_SECRET_ACCESS_KEY", "").strip()

    if endpoint_url:
        kwargs["endpoint_url"] = endpoint_url
    if access_key and secret_key:
        kwargs["aws_access_key_id"] = access_key
        kwargs["aws_secret_access_key"] = secret_key

    return boto3.client("s3", **kwargs)


def _upload_to_s3(key: str, body: bytes, content_type: str) -> None:
    bucket = current_app.config.get("AWS_S3_BUCKET", "").strip()
    if not bucket:
        raise ValueError("AWS_S3_BUCKET is required when STORAGE_BACKEND=s3")

    client = _s3_client()
    try:
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=body,
            ContentType=content_type,
        )
    except (BotoCoreError, ClientError) as exc:
        raise ValueError(f"S3 upload failed: {exc}") from exc


def _delete_from_s3(key: str) -> None:
    bucket = current_app.config.get("AWS_S3_BUCKET", "").strip()
    if not bucket or not key:
        return

    client = _s3_client()
    try:
        client.delete_object(Bucket=bucket, Key=key)
    except (BotoCoreError, ClientError):
        pass


# ─────────────────────────────────────────────────────────────────────────────
# Full upload pipeline  (convenience wrapper used by image_routes)
# ─────────────────────────────────────────────────────────────────────────────

def save_product_image(file: FileStorage) -> dict | None:
    """
    Validate, save, and thumbnail a single uploaded FileStorage object.

    Returns a dict with keys:
        filename, thumbnail, image_url, thumbnail_url, file_size, mime_type
    or raises ValueError with a user-facing message on failure.
    """
    ok, err, mime = validate_image(file)
    if not ok:
        raise ValueError(err)

    upload_folder: str = current_app.config["UPLOAD_FOLDER"]
    thumb_folder: str = current_app.config["THUMBNAIL_FOLDER"]
    thumb_size: tuple = current_app.config["THUMBNAIL_SIZE"]
    storage_backend = _get_storage_backend()

    # Build unique filenames
    fname, thumb_name = build_filenames(file.filename or "image", mime)

    # Read bytes once (validate_image already seeked back to 0)
    file.seek(0)
    file_bytes = file.read()
    thumb_bytes = generate_thumbnail_bytes(file_bytes, size=thumb_size)

    if storage_backend == "s3":
        prefix = current_app.config.get("S3_MEDIA_PREFIX", "uploads").strip("/")
        image_key = f"{prefix}/products/{fname}"
        thumb_key = f"{prefix}/thumbnails/{thumb_name}"

        _upload_to_s3(image_key, file_bytes, mime)
        _upload_to_s3(thumb_key, thumb_bytes, "image/jpeg")

        image_url = _build_s3_url(image_key)
        thumbnail_url = _build_s3_url(thumb_key)
        stored_image_name = image_key
        stored_thumb_name = thumb_key
    else:
        # Absolute on-disk paths
        os.makedirs(upload_folder, exist_ok=True)
        os.makedirs(thumb_folder, exist_ok=True)

        img_path = os.path.join(upload_folder, fname)
        thumb_path = os.path.join(thumb_folder, thumb_name)

        # Save original
        with open(img_path, "wb") as f:
            f.write(file_bytes)

        # Save generated thumbnail
        with open(thumb_path, "wb") as f:
            f.write(thumb_bytes)

        image_url = f"/uploads/products/{fname}"
        thumbnail_url = f"/uploads/thumbnails/{thumb_name}"
        stored_image_name = fname
        stored_thumb_name = thumb_name

    return {
        "filename": stored_image_name,
        "thumbnail": stored_thumb_name,
        "image_url": image_url,
        "thumbnail_url": thumbnail_url,
        "file_size": len(file_bytes),
        "mime_type": mime,
    }


def delete_stored_image(image_name: str, thumbnail_name: str) -> None:
    """Delete stored product image and thumbnail for local or S3 backends."""
    storage_backend = _get_storage_backend()

    if storage_backend == "s3":
        _delete_from_s3(image_name)
        _delete_from_s3(thumbnail_name)
        return

    upload_folder = current_app.config["UPLOAD_FOLDER"]
    thumb_folder = current_app.config["THUMBNAIL_FOLDER"]
    _try_delete(os.path.join(upload_folder, image_name))
    _try_delete(os.path.join(thumb_folder, thumbnail_name))


def _try_delete(path: str) -> None:
    """Delete a file silently if it exists."""
    try:
        if os.path.isfile(path):
            os.remove(path)
    except OSError:
        pass
