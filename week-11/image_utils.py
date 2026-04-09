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

def generate_thumbnail(image_bytes: bytes, thumb_path: str, size: tuple = (300, 300)) -> None:
    """
    Create a thumbnail from raw image bytes and save it to *thumb_path*.

    Algorithm:
      • Open the image with Pillow.
      • Convert RGBA / palette images → RGB so JPEG can be written.
      • thumbnail() resizes *in-place*, preserving aspect ratio, so the
        result fits within *size* without cropping.
      • Save as JPEG (quality=85) for consistent small file size.

    Args:
        image_bytes: Raw bytes of the original image.
        thumb_path:  Absolute filesystem path where the thumbnail is saved.
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

    # Ensure parent directory exists
    os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
    img.save(thumb_path, "JPEG", quality=85, optimize=True)


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
    thumb_folder: str  = current_app.config["THUMBNAIL_FOLDER"]
    thumb_size: tuple  = current_app.config["THUMBNAIL_SIZE"]

    # Build unique filenames
    fname, thumb_name = build_filenames(file.filename or "image", mime)

    # Absolute on-disk paths
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(thumb_folder, exist_ok=True)

    img_path   = os.path.join(upload_folder, fname)
    thumb_path = os.path.join(thumb_folder, thumb_name)

    # Read bytes once (validate_image already seeked back to 0)
    file.seek(0)
    file_bytes = file.read()

    # Save original
    with open(img_path, "wb") as f:
        f.write(file_bytes)

    # Generate & save thumbnail
    generate_thumbnail(file_bytes, thumb_path, size=thumb_size)

    return {
        "filename":      fname,
        "thumbnail":     thumb_name,
        "image_url":     f"/uploads/products/{fname}",
        "thumbnail_url": f"/uploads/thumbnails/{thumb_name}",
        "file_size":     len(file_bytes),
        "mime_type":     mime,
    }
