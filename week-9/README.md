# Week 9: E-commerce Backend (Buyer/Seller + JWT)

Flask + SQLAlchemy + PostgreSQL backend for an e-commerce workflow with:
- Buyer/Seller roles
- JWT auth
- Product search/filters/pagination
- Cart checkout that deducts stock
- Aggregation endpoints

## Role Model

- `1` = seller
- `2` = buyer

Rules:
- Only sellers can create/update/delete products.
- Both buyers and sellers can view products.
- Out-of-stock products are hidden from product listings.
- Checkout (`status=completed`) deducts product stock.

## Tech Stack

- Flask
- Flask-JWT-Extended
- SQLAlchemy + Flask-SQLAlchemy
- PostgreSQL (Docker Compose)

## Project Structure

```text
week-9/
  main.py
  auth.py
  crud.py
  models.py
  serializers.py
  config.py
  database.py
  schema.sql
  api.postman_collection.json
  routes/
    __init__.py
    auth_routes.py
    product_routes.py
    category_routes.py
    cart_routes.py
    aggregation_routes.py
```

## Run Locally

1. Start PostgreSQL:

```bash
docker-compose up -d
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run API:

```bash
python main.py
```

4. Base URL:

`http://127.0.0.1:5000`

## Important Database Note

Schema changed to include `seller_id` on products and role constraints.
If you already had an old DB volume, reset in dev:

```bash
docker-compose down -v
docker-compose up -d
```

## Auth Endpoints

### Register
`POST /api/auth/register`

Body example:

```json
{
  "name": "Sara Seller",
  "email": "sara@example.com",
  "password": "StrongPass123",
  "role": 1
}
```

`role` accepts `1|2` or `seller|buyer`.

### Login
`POST /api/auth/login`

```json
{
  "email": "sara@example.com",
  "password": "StrongPass123"
}
```

### Current User
`GET /api/auth/me` (JWT required)

### Validate Token
`GET /api/auth/validate` (JWT required)

Use this header format on all JWT-protected endpoints:

```http
Authorization: Bearer <access_token>
```

If token is missing or malformed (for example `Bearer undefined`), API returns `401 Unauthorized` with a hint message.

## Product Endpoints

### Public Listing
`GET /api/products`

Supported query params:
- `search`
- `category_id`
- `min_price`
- `max_price`
- `in_stock=true`
- `sort_by=price|name|created_at`
- `sort_order=asc|desc`
- `page`
- `per_page`

Behavior:
- Only `stock > 0` products are returned.

### Product Detail
`GET /api/products/{id}`

Behavior:
- Returns `404` if product is out of stock.

### Seller-only Product Management
- `POST /api/products`
- `PUT /api/products/{id}`
- `DELETE /api/products/{id}`

JWT required and seller role required.
Seller can modify only own products.

## Category Endpoints

- `POST /api/categories` (seller JWT required)
- `GET /api/categories`
- `GET /api/categories/{id}`
- `PUT /api/categories/{id}` (seller JWT required)
- `DELETE /api/categories/{id}` (seller JWT required)

Category detail endpoint returns only in-stock products for that category.

## Cart Endpoints (JWT Required)

- `POST /api/carts` (creates cart for authenticated user)
- `GET /api/carts`
- `GET /api/carts/{id}`
- `POST /api/carts/{id}/items`
- `PUT /api/carts/{id}/items/{item_id}`
- `DELETE /api/carts/{id}/items/{item_id}`
- `POST /api/carts/{id}/clear`
- `PUT /api/carts/{id}/status`
- `DELETE /api/carts/{id}`

Behavior:
- Users can access only their own carts.
- On `status=completed`, stock is validated then deducted.
- Repeating `completed` does not deduct stock twice.

## Aggregation Endpoints

- `GET /api/aggregations/stats`
- `GET /api/aggregations/category-breakdown`
- `GET /api/aggregations/price-distribution`
- `GET /api/aggregations/cart-analytics`

## Postman

Import `api.postman_collection.json` and run in this order:
1. Register seller
2. Login seller
3. Create product
4. Register buyer
5. Login buyer
6. Browse products
7. Create cart and checkout

## Known Design Choices

- Auth and role checks are enforced at route level.
- `crud.py` contains shared business operations (public product query and checkout stock deduction).
- User CRUD endpoints were removed from active API as requested.
