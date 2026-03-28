# Week 9: E-commerce Backend Skeleton

A basic Flask + SQLAlchemy API skeleton for:
- Products
- Categories
- Users
- Carts
- Product search and filters (price/category)
- Pagination
- Aggregation endpoint

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

API base URL: `http://127.0.0.1:5000`

## Implemented Endpoints

### Health
- `GET /`

### Categories
- `POST /api/categories`
- `GET /api/categories`

### Users
- `POST /api/users`
- `GET /api/users`

### Products
- `POST /api/products`
- `GET /api/products`
- `GET /api/products/<product_id>`
- `GET /api/products/aggregations/by-category`

### Carts
- `POST /api/carts`
- `POST /api/carts/<cart_id>/items`
- `GET /api/carts/<cart_id>`

## Product Search / Filters / Pagination

`GET /api/products` supports:
- `q`: keyword match on product name/description
- `category_id`: filter by category
- `min_price`: minimum price
- `max_price`: maximum price
- `page`: page number (default `1`)
- `per_page`: page size (default `10`, max `100`)

Example:

```bash
curl "http://127.0.0.1:5000/api/products?q=phone&category_id=1&min_price=100&max_price=1500&page=1&per_page=5"
```

## Notes
- Uses SQLite by default (`ecommerce.db` file).
- Database tables are auto-created on startup via `db.create_all()`.
- `schema.sql` is included for a SQL-first setup if needed.
