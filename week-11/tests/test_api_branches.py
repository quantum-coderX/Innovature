import io

from database import db
from models import Cart, CartItem, Category, Product


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


def test_auth_error_branches(client, app, make_user):
    bad_register = client.post(
        "/api/auth/register",
        json={"name": "x", "email": "bad", "password": "123", "role": "invalid"},
    )
    assert bad_register.status_code == 400

    with app.app_context():
        make_user(email="inactive@example.com", role=2, is_active=False)

    login_missing = client.post("/api/auth/login", json={"email": "", "password": ""})
    assert login_missing.status_code == 400

    login_invalid = client.post(
        "/api/auth/login",
        json={"email": "inactive@example.com", "password": "badpass"},
    )
    assert login_invalid.status_code == 400

    login_inactive = client.post(
        "/api/auth/login",
        json={"email": "inactive@example.com", "password": "password123"},
    )
    assert login_inactive.status_code == 400


def test_category_routes_branches(client, app, make_user, make_category, make_product, make_auth_header):
    with app.app_context():
        seller = make_user(email="cat-owner@example.com", role=1)
        other_seller = make_user(email="other-cat-owner@example.com", role=1)
        category = make_category(name="Books")
        other_category = make_category(name="Music")
        make_product(
            seller_id=seller.id,
            category_id=category.id,
            name="Book Item",
            stock=2,
            sku="BOOK-1",
        )

    seller_headers = make_auth_header(seller.id, role_code=seller.role)
    other_headers = make_auth_header(other_seller.id, role_code=other_seller.role)

    duplicate = client.post("/api/categories", headers=seller_headers, json={"name": "Books"})
    assert duplicate.status_code == 400

    listing = client.get("/api/categories?page=-1&per_page=999")
    assert listing.status_code == 200

    detail = client.get(f"/api/categories/{category.id}")
    assert detail.status_code == 200
    assert detail.get_json()["data"]["products_count"] == 1

    not_found = client.get("/api/categories/9999")
    assert not_found.status_code == 404

    update_dup = client.put(
        f"/api/categories/{category.id}",
        headers=seller_headers,
        json={"name": other_category.name},
    )
    assert update_dup.status_code == 400

    update_ok = client.put(
        f"/api/categories/{category.id}",
        headers=seller_headers,
        json={"description": "Updated"},
    )
    assert update_ok.status_code == 200

    conflict_delete = client.delete(f"/api/categories/{category.id}", headers=other_headers)
    assert conflict_delete.status_code == 409


def test_product_route_branches(client, app, make_user, make_category, make_product, make_auth_header):
    with app.app_context():
        seller = make_user(email="p-seller@example.com", role=1)
        another = make_user(email="p-another@example.com", role=1)
        buyer = make_user(email="p-buyer@example.com", role=2)
        cat = make_category(name="Home")
        product = make_product(seller_id=seller.id, category_id=cat.id, name="Lamp", stock=1, sku="LAMP-1")

    seller_headers = make_auth_header(seller.id, role_code=seller.role)
    another_headers = make_auth_header(another.id, role_code=another.role)
    buyer_headers = make_auth_header(buyer.id, role_code=buyer.role)

    forbidden = client.post("/api/products", headers=buyer_headers, json={"name": "x"})
    assert forbidden.status_code == 403

    bad_price = client.post(
        "/api/products",
        headers=seller_headers,
        json={"name": "A", "price": -1, "stock": 1, "category_id": cat.id},
    )
    assert bad_price.status_code == 400

    bad_stock = client.post(
        "/api/products",
        headers=seller_headers,
        json={"name": "A", "price": 2, "stock": "x", "category_id": cat.id},
    )
    assert bad_stock.status_code == 400

    bad_category = client.get("/api/products?category_id=9999")
    assert bad_category.status_code == 400

    out_of_stock = client.put(
        f"/api/products/{product.id}",
        headers=seller_headers,
        json={"stock": 0},
    )
    assert out_of_stock.status_code == 200

    hidden = client.get(f"/api/products/{product.id}")
    assert hidden.status_code == 404

    forbidden_update = client.put(
        f"/api/products/{product.id}",
        headers=another_headers,
        json={"name": "x"},
    )
    assert forbidden_update.status_code == 403


def test_cart_route_branches(client, app, make_user, make_category, make_product, make_auth_header):
    with app.app_context():
        seller = make_user(email="cart2-seller@example.com", role=1)
        buyer = make_user(email="cart2-buyer@example.com", role=2)
        other_buyer = make_user(email="cart2-other@example.com", role=2)
        cat = make_category(name="Gaming")
        p1 = make_product(seller_id=seller.id, category_id=cat.id, name="Pad", stock=4, sku="PAD-1")

    buyer_headers = make_auth_header(buyer.id, role_code=buyer.role)
    other_headers = make_auth_header(other_buyer.id, role_code=other_buyer.role)

    cart_create = client.post("/api/carts", headers=buyer_headers)
    assert cart_create.status_code == 201
    cart_id = cart_create.get_json()["data"]["id"]

    list_carts = client.get("/api/carts?status=open&page=-2&per_page=200", headers=buyer_headers)
    assert list_carts.status_code == 200

    forbidden_cart = client.get(f"/api/carts/{cart_id}", headers=other_headers)
    assert forbidden_cart.status_code == 403

    missing_product = client.post(
        f"/api/carts/{cart_id}/items",
        headers=buyer_headers,
        json={"quantity": 1},
    )
    assert missing_product.status_code == 400

    add_ok = client.post(
        f"/api/carts/{cart_id}/items",
        headers=buyer_headers,
        json={"product_id": p1.id, "quantity": 1},
    )
    assert add_ok.status_code == 201
    item_id = add_ok.get_json()["data"]["items"][0]["id"]

    add_too_many = client.post(
        f"/api/carts/{cart_id}/items",
        headers=buyer_headers,
        json={"product_id": p1.id, "quantity": 99},
    )
    assert add_too_many.status_code == 400

    update_bad = client.put(
        f"/api/carts/{cart_id}/items/{item_id}",
        headers=buyer_headers,
        json={"quantity": 0},
    )
    assert update_bad.status_code == 400

    update_ok = client.put(
        f"/api/carts/{cart_id}/items/{item_id}",
        headers=buyer_headers,
        json={"quantity": 2},
    )
    assert update_ok.status_code == 200

    clear_ok = client.post(f"/api/carts/{cart_id}/clear", headers=buyer_headers)
    assert clear_ok.status_code == 200

    complete_empty = client.put(
        f"/api/carts/{cart_id}/status",
        headers=buyer_headers,
        json={"status": "completed"},
    )
    assert complete_empty.status_code == 400

    add_again = client.post(
        f"/api/carts/{cart_id}/items",
        headers=buyer_headers,
        json={"product_id": p1.id, "quantity": 1},
    )
    assert add_again.status_code == 201

    invalid_status = client.put(
        f"/api/carts/{cart_id}/status",
        headers=buyer_headers,
        json={"status": "invalid"},
    )
    assert invalid_status.status_code == 400

    checkout_status = client.put(
        f"/api/carts/{cart_id}/status",
        headers=buyer_headers,
        json={"status": "checkout"},
    )
    assert checkout_status.status_code == 200

    cannot_add_checkout = client.post(
        f"/api/carts/{cart_id}/items",
        headers=buyer_headers,
        json={"product_id": p1.id, "quantity": 1},
    )
    assert cannot_add_checkout.status_code == 400

    remove_item = client.delete(
        f"/api/carts/{cart_id}/items/{add_again.get_json()['data']['items'][0]['id']}",
        headers=buyer_headers,
    )
    assert remove_item.status_code == 200

    delete_cart = client.delete(f"/api/carts/{cart_id}", headers=buyer_headers)
    assert delete_cart.status_code == 200


def test_image_route_error_branches(client, app, monkeypatch, make_user, make_category, make_product, make_auth_header):
    with app.app_context():
        seller = make_user(email="img-err-seller@example.com", role=1)
        other_seller = make_user(email="img-err-other@example.com", role=1)
        cat = make_category(name="Phones")
        product = make_product(seller_id=seller.id, category_id=cat.id, name="Phone", stock=3, sku="PHONE-1")

    seller_headers = make_auth_header(seller.id, role_code=seller.role)
    other_headers = make_auth_header(other_seller.id, role_code=other_seller.role)

    no_files = client.post(f"/api/products/{product.id}/images", headers=seller_headers)
    assert no_files.status_code == 400

    forbidden = client.post(
        f"/api/products/{product.id}/images",
        headers=other_headers,
        data={"images": (io.BytesIO(b"x"), "a.jpg")},
        content_type="multipart/form-data",
    )
    assert forbidden.status_code == 403

    def fail_save(_file):
        raise ValueError("Invalid file type. Allowed types: image/jpeg")

    monkeypatch.setattr("routes.image_routes.save_product_image", fail_save)

    all_fail = client.post(
        f"/api/products/{product.id}/images",
        headers=seller_headers,
        data={"images": (io.BytesIO(b"x"), "bad.txt")},
        content_type="multipart/form-data",
    )
    assert all_fail.status_code == 400

    missing_product = client.get("/api/products/9999/images")
    assert missing_product.status_code == 404


def test_aggregation_error_branch(client, monkeypatch):
    def boom(*args, **kwargs):
        raise RuntimeError("db down")

    monkeypatch.setattr("routes.aggregation_routes.Product.query.count", boom)
    res = client.get("/api/aggregations/stats")
    assert res.status_code == 500
