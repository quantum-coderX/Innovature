# Project Summary

## Final State

Week-9 backend now runs as a buyer/seller marketplace with JWT and stock-aware checkout.

## Implemented

- Buyer/Seller roles (`1=seller`, `2=buyer`)
- JWT auth (`register`, `login`, `me`, `validate`)
- Seller-only product create/update/delete
- Public product browsing with search/filter/pagination
- Out-of-stock products hidden from listing and blocked on detail endpoint
- Cart checkout reduces stock when status is marked `completed`
- Own-cart-only access control
- Aggregation endpoints
- `crud.py` for shared business operations

## Intentional Removals

- User CRUD endpoints are not active in route registration

## Integrity Updates

Schema constraints added for:
- role domain
- stock non-negative
- quantity positive
- cart status domain

## Documentation Sync

Updated:
- README
- ARCHITECTURE
- QUICKSTART
- Postman collection
