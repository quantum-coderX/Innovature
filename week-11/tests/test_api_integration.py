import io
from decimal import Decimal

from database import db
from models import CartItem, Product, ProductImage


def _register_and_login(client, *, name, email, password, role):
    reg = client.post(
        "/api/auth/register",
        json={"name": name, "email": email, "password": password, "role": role},
    )
    assert reg.status_code == 201

    login = client.post("/api/auth/login", json={"email": email, "password": password})
    assert login.status_code == 200
    token = login.get_json()["data"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_auth_me_validate_and_unauthorized(client):
    res = client.get("/api/auth/me")
    assert res.status_code == 401

    headers = _register_and_login(
        client,
        name="Seller",
        email="seller.flow@example.com",
        password="password123",
        role="seller",
    )

    me = client.get("/api/auth/me", headers=headers)
    assert me.status_code == 200
    assert me.get_json()["data"]["email"] == "seller.flow@example.com"

    validate = client.get("/api/auth/validate", headers=headers)
    assert validate.status_code == 200
    assert validate.get_json()["data"]["valid"] is True


def test_category_and_product_crud_flow(client):
    seller_headers = _register_and_login(
        client,
        name="Category Seller",
        email="cat-seller@example.com",
        password="password123",
        role="seller",
    )

    category_res = client.post(
        "/api/categories",
        headers=seller_headers,
        json={"name": "Electronics", "description": "Devices"},
    )
    assert category_res.status_code == 201
    category_id = category_res.get_json()["data"]["id"]

    product_res = client.post(
        "/api/products",
        headers=seller_headers,
        json={
            "name": "Keyboard",
            "description": "Mechanical",
            "price": 120,
            "stock": 8,
            "category_id": category_id,
            "sku": "KEY-1",
        },
    )
    assert product_res.status_code == 201
    product_id = product_res.get_json()["data"]["id"]

    list_res = client.get("/api/products?search=key&sort_by=price&sort_order=asc")
    assert list_res.status_code == 200
    assert list_res.get_json()["pagination"]["total"] >= 1

    detail = client.get(f"/api/products/{product_id}")
    assert detail.status_code == 200
    assert detail.get_json()["data"]["name"] == "Keyboard"

    update = client.put(
        f"/api/products/{product_id}",
        headers=seller_headers,
        json={"stock": 10, "price": 150},
    )
    assert update.status_code == 200
    assert update.get_json()["data"]["stock"] == 10


def test_cart_checkout_flow_reduces_stock(client, app, make_user, make_category, make_product, make_auth_header):
    with app.app_context():
        seller = make_user(email="cart-seller@example.com", role=1)
        buyer = make_user(email="cart-buyer@example.com", role=2)
        category = make_category(name="Peripherals")
        product = make_product(
            seller_id=seller.id,
            category_id=category.id,
            name="Mouse",
            price="60.00",
            stock=5,
            sku="MOUSE-1",
        )

    buyer_headers = make_auth_header(buyer.id, role_code=buyer.role)

    create_cart = client.post("/api/carts", headers=buyer_headers)
    assert create_cart.status_code == 201
    cart_id = create_cart.get_json()["data"]["id"]

    add_item = client.post(
        f"/api/carts/{cart_id}/items",
        headers=buyer_headers,
        json={"product_id": product.id, "quantity": 2},
    )
    assert add_item.status_code == 201

    complete = client.put(
        f"/api/carts/{cart_id}/status",
        headers=buyer_headers,
        json={"status": "completed"},
    )
    assert complete.status_code == 200

    with app.app_context():
        refreshed = db.session.get(Product, product.id)
        assert refreshed.stock == 3


def test_image_routes_with_mocked_external_processor(client, app, monkeypatch, make_user, make_category, make_product, make_auth_header):
    # Mocking the image processing dependency to simulate an external service.
    def fake_save_product_image(_file):
        return {
            "filename": "mocked_image.jpg",
            "thumbnail": "thumb_mocked_image.jpg",
            "image_url": "/uploads/products/mocked_image.jpg",
            "thumbnail_url": "/uploads/thumbnails/thumb_mocked_image.jpg",
            "file_size": 111,
            "mime_type": "image/jpeg",
        }

    monkeypatch.setattr("routes.image_routes.save_product_image", fake_save_product_image)

    with app.app_context():
        seller = make_user(email="img-seller@example.com", role=1)
        category = make_category(name="Cameras")
        product = make_product(
            seller_id=seller.id,
            category_id=category.id,
            name="DSLR",
            price=Decimal("500.00"),
            stock=4,
            sku="CAM-1",
        )

    seller_headers = make_auth_header(seller.id, role_code=seller.role)

    data = {"images": (io.BytesIO(b"dummy-image"), "photo.jpg")}
    upload = client.post(
        f"/api/products/{product.id}/images",
        headers=seller_headers,
        data=data,
        content_type="multipart/form-data",
    )
    assert upload.status_code == 201
    payload = upload.get_json()["data"]
    assert payload["total_images"] == 1
    image_id = payload["uploaded"][0]["id"]

    listed = client.get(f"/api/products/{product.id}/images")
    assert listed.status_code == 200
    assert listed.get_json()["data"]["count"] == 1

    make_primary = client.patch(
        f"/api/products/{product.id}/images/{image_id}/primary",
        headers=seller_headers,
    )
    assert make_primary.status_code == 200

    delete_res = client.delete(
        f"/api/products/{product.id}/images/{image_id}",
        headers=seller_headers,
    )
    assert delete_res.status_code == 200

    with app.app_context():
        assert ProductImage.query.filter_by(product_id=product.id).count() == 0


def test_aggregation_endpoints(client, app, make_user, make_category, make_product):
    with app.app_context():
        seller = make_user(email="agg-seller@example.com", role=1)
        buyer = make_user(email="agg-buyer@example.com", role=2)
        category = make_category(name="Office")
        product = make_product(
            seller_id=seller.id,
            category_id=category.id,
            name="Desk",
            price="200",
            stock=7,
            sku="DESK-1",
        )

        from models import Cart

        cart = Cart(user_id=buyer.id, status="open")
        db.session.add(cart)
        db.session.flush()
        db.session.add(CartItem(cart_id=cart.id, product_id=product.id, quantity=2, unit_price=Decimal("200")))
        db.session.commit()

    stats = client.get("/api/aggregations/stats")
    assert stats.status_code == 200
    assert stats.get_json()["data"]["total_products"] >= 1

    category_breakdown = client.get("/api/aggregations/category-breakdown")
    assert category_breakdown.status_code == 200
    assert category_breakdown.get_json()["data"]["total_categories"] >= 1

    price_distribution = client.get("/api/aggregations/price-distribution")
    assert price_distribution.status_code == 200
    assert len(price_distribution.get_json()["data"]["price_distribution"]) == 6

    cart_analytics = client.get("/api/aggregations/cart-analytics")
    assert cart_analytics.status_code == 200
    assert "popular_products" in cart_analytics.get_json()["data"]
