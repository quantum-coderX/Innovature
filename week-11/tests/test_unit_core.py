from decimal import Decimal
from io import BytesIO

import pytest
from werkzeug.datastructures import FileStorage

from auth import ROLE_BUYER, ROLE_SELLER, hash_password, parse_role_code, verify_password
from crud import checkout_cart
from database import db
from image_utils import _safe_stem, build_filenames, save_product_image, validate_image
from models import Cart, CartItem, ProductImage


def _jpeg_bytes():
    return (
        b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
        b"\xff\xdb\x00C\x00" + b"\x08" * 67 + b"\xff\xd9"
    )


def test_parse_role_code_variants():
    assert parse_role_code(None, default=ROLE_BUYER) == ROLE_BUYER
    assert parse_role_code("seller") == ROLE_SELLER
    assert parse_role_code("buyer") == ROLE_BUYER
    assert parse_role_code("1") == ROLE_SELLER
    assert parse_role_code(2) == ROLE_BUYER
    assert parse_role_code("invalid") is None


def test_password_hash_and_verify():
    digest = hash_password("my-password")
    assert digest != "my-password"
    assert verify_password(digest, "my-password") is True
    assert verify_password(digest, "wrong") is False
    assert verify_password("", "x") is False


def test_checkout_cart_validation_and_stock_deduction(app, make_user, make_category, make_product):
    with app.app_context():
        buyer = make_user(email="buyer@example.com", role=ROLE_BUYER)
        seller = make_user(email="seller@example.com", role=ROLE_SELLER)
        category = make_category(name="Audio")
        product = make_product(
            seller_id=seller.id,
            category_id=category.id,
            stock=10,
            price="99.99",
            sku="SKU-A",
        )

        cart = Cart(user_id=buyer.id, status="open")
        db.session.add(cart)
        db.session.flush()

        item = CartItem(cart_id=cart.id, product_id=product.id, quantity=3, unit_price=Decimal("99.99"))
        db.session.add(item)
        db.session.commit()

        checkout_cart(cart)
        assert product.stock == 7


def test_checkout_cart_errors(app, make_user):
    with app.app_context():
        buyer = make_user(email="empty-cart@example.com", role=ROLE_BUYER)
        cart = Cart(user_id=buyer.id, status="open")
        db.session.add(cart)
        db.session.commit()

        with pytest.raises(ValueError, match="Cart is empty"):
            checkout_cart(cart)


def test_filename_builder_and_safe_stem():
    stem = _safe_stem("../../my summer photo!!.png")
    assert ".." not in stem
    assert " " not in stem

    filename, thumb = build_filenames("my file.png", "image/png")
    assert filename.endswith(".png")
    assert thumb.startswith("thumb_")
    assert thumb.endswith(".jpg")


def test_validate_image_success_and_invalid_type(app):
    with app.app_context():
        valid = FileStorage(stream=BytesIO(_jpeg_bytes()), filename="ok.jpg")
        ok, err, mime = validate_image(valid)
        assert ok is True
        assert err is None
        assert mime == "image/jpeg"

        invalid = FileStorage(stream=BytesIO(b"not-image"), filename="doc.txt")
        ok, err, mime = validate_image(invalid)
        assert ok is False
        assert "Invalid file type" in err
        assert mime is None


def test_save_product_image_pipeline_with_mocked_thumbnail(app, monkeypatch):
    calls = {}

    def fake_generate_thumbnail(image_bytes, thumb_path, size=(300, 300)):
        calls["thumb_path"] = thumb_path
        calls["size"] = size
        with open(thumb_path, "wb") as fp:
            fp.write(b"thumb")

    monkeypatch.setattr("image_utils.generate_thumbnail", fake_generate_thumbnail)

    with app.app_context():
        upload = FileStorage(stream=BytesIO(_jpeg_bytes()), filename="camera.jpg")

        meta = save_product_image(upload)
        assert meta["filename"].endswith(".jpg")
        assert meta["thumbnail"].startswith("thumb_")
        assert meta["mime_type"] == "image/jpeg"
        assert "/uploads/products/" in meta["image_url"]
        assert calls["size"] == app.config["THUMBNAIL_SIZE"]


def test_product_image_repr(app, make_user, make_category, make_product):
    with app.app_context():
        seller = make_user(email="seller2@example.com", role=ROLE_SELLER)
        category = make_category(name="Phones")
        product = make_product(seller_id=seller.id, category_id=category.id, sku="SKU-B")

        img = ProductImage(
            product_id=product.id,
            filename="x.jpg",
            thumbnail="thumb_x.jpg",
            image_url="/uploads/products/x.jpg",
            thumbnail_url="/uploads/thumbnails/thumb_x.jpg",
            is_primary=True,
        )
        db.session.add(img)
        db.session.commit()

        assert "ProductImage" in repr(img)
