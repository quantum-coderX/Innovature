from datetime import datetime, timezone
from database import db


def utc_now():
    """Get current UTC time as timezone-aware datetime"""
    return datetime.now(timezone.utc)


def ensure_aware(dt):
    """Convert naive datetime to aware UTC datetime"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt


class Category(db.Model):
    """Category model for product organization"""
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships
    products = db.relationship("Product", backref="category", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Category {self.name}>'


class User(db.Model):
    """User model for buyers and sellers"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=True)
    role = db.Column(db.Integer, nullable=False, default=2, index=True)  # 1=seller, 2=buyer
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships
    carts = db.relationship("Cart", backref="user", lazy=True, cascade="all, delete-orphan")
    products = db.relationship("Product", backref="seller", lazy=True)

    def __repr__(self):
        return f'<User {self.email}>'


class Product(db.Model):
    """Product model with price and stock tracking"""
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False, index=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    sku = db.Column(db.String(100), unique=True, nullable=True, index=True)
    seller_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships
    cart_items = db.relationship("CartItem", backref="product", lazy=True)
    images = db.relationship(
        "ProductImage",
        backref="product",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="ProductImage.is_primary.desc(), ProductImage.created_at.asc()"
    )

    def __repr__(self):
        return f'<Product {self.name}>'


# ─────────────────────────────────────────────────────────────────────────────
# ProductImage  (Week 10 addition)
# ─────────────────────────────────────────────────────────────────────────────

class ProductImage(db.Model):
    """
    Stores metadata for each uploaded product image.

    The actual files live on-disk:
      static/uploads/products/<filename>
      static/uploads/thumbnails/<thumbnail>

    image_url / thumbnail_url are relative URL paths served by Flask
    (e.g.  /uploads/products/abc123_photo.jpg)
    """
    __tablename__ = "product_image"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer,
        db.ForeignKey("product.id"),
        nullable=False,
        index=True,
    )

    # ── stored filenames (disk) ──────────────────────────────────
    filename = db.Column(db.String(255), nullable=False)       # e.g. uuid4_photo.jpg
    thumbnail = db.Column(db.String(255), nullable=False)      # e.g. thumb_uuid4_photo.jpg

    # ── public URL paths (served by Flask) ──────────────────────
    image_url = db.Column(db.String(512), nullable=False)      # /uploads/products/...
    thumbnail_url = db.Column(db.String(512), nullable=False)  # /uploads/thumbnails/...

    # ── file metadata ────────────────────────────────────────────
    file_size = db.Column(db.Integer, nullable=True)           # bytes
    mime_type = db.Column(db.String(50), nullable=True)        # image/jpeg etc.

    # ── ordering / presentation ──────────────────────────────────
    is_primary = db.Column(db.Boolean, nullable=False, default=False)

    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)

    def __repr__(self):
        return f'<ProductImage {self.id} product={self.product_id} primary={self.is_primary}>'


class Cart(db.Model):
    """Shopping cart model"""
    __tablename__ = "cart"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, index=True)
    status = db.Column(db.String(20), nullable=False, default="open")  # open, checkout, completed, abandoned
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    # Relationships
    items = db.relationship("CartItem", backref="cart", lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Cart {self.id} - User {self.user_id}>'


class CartItem(db.Model):
    """Individual items in a cart"""
    __tablename__ = "cart_item"

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=utc_now, nullable=False)
    updated_at = db.Column(db.DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    def __repr__(self):
        return f'<CartItem {self.id}>'
