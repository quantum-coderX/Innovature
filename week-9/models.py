from datetime import datetime, timezone
from database import db


def utc_now():
    return datetime.now(timezone.utc)


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    products = db.relationship("Product", backref="category", lazy=True)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    carts = db.relationship("Cart", backref="user", lazy=True)


class Product(db.Model):
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False, index=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)


class Cart(db.Model):
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="open")
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    items = db.relationship("CartItem", backref="cart", lazy=True, cascade="all, delete-orphan")


class CartItem(db.Model):
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False)

    product = db.relationship("Product")
