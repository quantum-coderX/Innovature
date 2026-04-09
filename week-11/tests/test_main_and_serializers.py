import os
from datetime import datetime, timezone

from database import db
from main import app
from models import ProductImage
from serializers import (
    error_response,
    paginated_response,
    serialize_product,
    serialize_product_image,
    success_response,
)


def test_main_routes_and_error_handlers(client):
    health = client.get("/")
    assert health.status_code == 200
    assert health.get_json()["status"] == "ok"

    not_found = client.get("/no-such-route")
    assert not_found.status_code == 404


def test_serve_uploaded_file(client, app):
    with app.app_context():
        root = os.path.join("d:\\Innovature\\week-11", "static", "uploads")
        products = os.path.join(root, "products")
        os.makedirs(products, exist_ok=True)
        path = os.path.join(products, "test.txt")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("ok")

    resp = client.get("/uploads/products/test.txt")
    assert resp.status_code == 200


def test_serializer_helpers_and_image_serialization(app, make_user, make_category, make_product):
    err, code = error_response("bad", 422)
    assert code == 422
    assert err["error"] == "bad"

    ok, code = success_response({"x": 1}, "done", 201)
    assert code == 201
    assert ok["message"] == "done"

    page, code = paginated_response([1, 2], page=1, per_page=2, total=3)
    assert code == 200
    assert page["pagination"]["has_next"] is True

    with app.app_context():
        seller = make_user(email="ser-seller@example.com", role=1)
        cat = make_category(name="Accessories")
        product = make_product(seller_id=seller.id, category_id=cat.id, name="Case", stock=5, sku="CASE-1")

        img1 = ProductImage(
            product_id=product.id,
            filename="a.jpg",
            thumbnail="thumb_a.jpg",
            image_url="/uploads/products/a.jpg",
            thumbnail_url="/uploads/thumbnails/thumb_a.jpg",
            is_primary=False,
            created_at=datetime.now(timezone.utc),
        )
        img2 = ProductImage(
            product_id=product.id,
            filename="b.jpg",
            thumbnail="thumb_b.jpg",
            image_url="/uploads/products/b.jpg",
            thumbnail_url="/uploads/thumbnails/thumb_b.jpg",
            is_primary=True,
            created_at=datetime.now(timezone.utc),
        )
        db.session.add_all([img1, img2])
        db.session.commit()

        one = serialize_product_image(img1)
        assert one["filename"] == "a.jpg"

        data = serialize_product(product)
        assert data["primary_image_url"] == "/uploads/products/b.jpg"
        assert len(data["images"]) == 2
