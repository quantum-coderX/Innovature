# Quickstart

## 1) Start database

```bash
docker-compose up -d
```

## 2) Install dependencies

```bash
pip install -r requirements.txt
```

## 3) Run API

```bash
python main.py
```

Base URL: `http://127.0.0.1:5000`

## 4) Smoke test

```bash
curl http://127.0.0.1:5000/
```

## 5) Register seller + login

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Seller One","email":"seller@example.com","password":"StrongPass123","role":1}'

curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"seller@example.com","password":"StrongPass123"}'
```

Use returned JWT in `Authorization: Bearer <token>`.

## 6) Seller creates product

```bash
curl -X POST http://127.0.0.1:5000/api/products \
  -H "Authorization: Bearer <SELLER_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Phone","description":"Demo","price":499.99,"stock":5,"sku":"PHONE-100","category_id":1}'
```

## 7) Register buyer + login

```bash
curl -X POST http://127.0.0.1:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Buyer One","email":"buyer@example.com","password":"StrongPass123","role":2}'

curl -X POST http://127.0.0.1:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"buyer@example.com","password":"StrongPass123"}'
```

## 8) Buyer checkout flow

```bash
# create cart
curl -X POST http://127.0.0.1:5000/api/carts -H "Authorization: Bearer <BUYER_TOKEN>"

# add item
curl -X POST http://127.0.0.1:5000/api/carts/1/items \
  -H "Authorization: Bearer <BUYER_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"quantity":2}'

# complete checkout (deducts stock)
curl -X PUT http://127.0.0.1:5000/api/carts/1/status \
  -H "Authorization: Bearer <BUYER_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"status":"completed"}'
```

## 9) If schema changed and old DB exists

```bash
docker-compose down -v
docker-compose up -d
```
