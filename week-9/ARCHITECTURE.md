# Architecture

## Overview

This API uses modular Flask blueprints with role-aware business rules.

- Authenticated identity: JWT (`Flask-JWT-Extended`)
- Roles: seller (1), buyer (2)
- Product ownership: each product belongs to one seller
- Checkout side effect: stock deduction at completion

## Modules

- `main.py`: app bootstrap, extension init, error handlers
- `auth.py`: role constants, password hashing, auth decorators
- `crud.py`: shared domain operations
- `models.py`: SQLAlchemy entities and relations
- `serializers.py`: response shaping
- `routes/*.py`: HTTP route handlers

## Blueprint Layout

- `auth_routes.py`: register/login/me/validate
- `product_routes.py`: public product browse + seller-only product management
- `category_routes.py`: category CRUD and category product listing
- `cart_routes.py`: authenticated cart operations, own-cart enforcement
- `aggregation_routes.py`: reporting/analytics endpoints

## Data Model

### User
- `id`, `name`, `email`, `password_hash`
- `role` (`1=seller`, `2=buyer`)
- `is_active`

### Product
- `seller_id` (FK -> user)
- `category_id` (FK -> category)
- `price`, `stock`, `sku`

### Cart/CartItem
- cart belongs to a user
- cart items reference products
- checkout decrements `product.stock`

## Access Control Rules

- Seller-only:
  - `POST /api/categories`
  - `PUT /api/categories/{id}`
  - `DELETE /api/categories/{id}`
  - `POST /api/products`
  - `PUT /api/products/{id}`
  - `DELETE /api/products/{id}`
- Public:
  - product browse/detail (with out-of-stock restrictions)
  - categories
  - aggregations
- Authenticated user only:
  - cart operations (own cart only)
  - auth profile/validate endpoints

## Inventory Behavior

- Public list shows only products with `stock > 0`.
- Product detail for `stock <= 0` returns not available.
- Category product list also excludes out-of-stock products.
- On cart completion (`status=completed`):
  1. Validate all item quantities against stock.
  2. Deduct stock atomically in the same transaction.

## Integrity Constraints in Schema

- `user.role IN (1,2)`
- `product.stock >= 0`
- `cart_item.quantity > 0`
- `cart.status IN ('open','checkout','completed','abandoned')`

## Design Notes

- Business operations centralized in `crud.py` to avoid route duplication.
- Role parsing accepts code or label at registration input for convenience.
- User CRUD routes intentionally not active in blueprint registration.
