"""CRUD helpers for core e-commerce workflows."""

from database import db
from models import Product


def get_public_products_query():
    """Products visible in marketplace: only in-stock items."""
    return Product.query.filter(Product.stock > 0)


def create_product_for_seller(*, seller_id, name, description, price, stock, sku, category_id):
    product = Product(
        seller_id=seller_id,
        name=name,
        description=description,
        price=price,
        stock=stock,
        sku=sku,
        category_id=category_id,
    )
    db.session.add(product)
    db.session.flush()
    return product


def checkout_cart(cart):
    """Validate cart stock and reduce product quantity atomically."""
    if not cart.items:
        raise ValueError('Cart is empty')

    for item in cart.items:
        if item.product.stock < item.quantity:
            raise ValueError(
                f'Insufficient stock for {item.product.name}. Available: {item.product.stock}'
            )

    for item in cart.items:
        item.product.stock -= item.quantity
