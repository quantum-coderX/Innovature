from flask import Flask, jsonify, request
from sqlalchemy import func
from config import Config
from database import db
from models import Category, Product, User, Cart, CartItem


app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


with app.app_context():
    db.create_all()


def product_to_dict(product):
    return {
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "stock": product.stock,
        "category_id": product.category_id,
        "category_name": product.category.name if product.category else None,
        "created_at": product.created_at.isoformat() if product.created_at else None,
    }


def cart_to_dict(cart):
    items = []
    total_amount = 0.0

    for item in cart.items:
        line_total = item.quantity * item.unit_price
        total_amount += line_total
        items.append(
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product.name if item.product else None,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "line_total": round(line_total, 2),
            }
        )

    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "status": cart.status,
        "created_at": cart.created_at.isoformat() if cart.created_at else None,
        "updated_at": cart.updated_at.isoformat() if cart.updated_at else None,
        "items": items,
        "total_amount": round(total_amount, 2),
    }


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Week 9 E-commerce API skeleton"}), 200


@app.route("/api/categories", methods=["POST"])
def create_category():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()

    if not name:
        return jsonify({"message": "Category name is required"}), 400

    if Category.query.filter_by(name=name).first():
        return jsonify({"message": "Category already exists"}), 409

    category = Category(name=name, description=data.get("description"))
    db.session.add(category)
    db.session.commit()

    return jsonify({"id": category.id, "name": category.name, "description": category.description}), 201


@app.route("/api/categories", methods=["GET"])
def list_categories():
    categories = Category.query.order_by(Category.name.asc()).all()
    return jsonify(
        [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description,
            }
            for category in categories
        ]
    ), 200


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()

    if not name or not email:
        return jsonify({"message": "Name and email are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 409

    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()

    return jsonify({"id": user.id, "name": user.name, "email": user.email}), 201


@app.route("/api/users", methods=["GET"])
def list_users():
    users = User.query.order_by(User.id.asc()).all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users]), 200


@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json() or {}

    name = (data.get("name") or "").strip()
    category_id = data.get("category_id")
    price = data.get("price")
    stock = data.get("stock", 0)

    if not name or category_id is None or price is None:
        return jsonify({"message": "name, category_id and price are required"}), 400

    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"message": "Category not found"}), 404

    try:
        price = float(price)
        stock = int(stock)
    except (TypeError, ValueError):
        return jsonify({"message": "price must be numeric and stock must be an integer"}), 400

    if price < 0 or stock < 0:
        return jsonify({"message": "price and stock must be non-negative"}), 400

    product = Product(
        name=name,
        description=data.get("description"),
        price=price,
        stock=stock,
        category_id=category_id,
    )
    db.session.add(product)
    db.session.commit()

    return jsonify(product_to_dict(product)), 201


@app.route("/api/products", methods=["GET"])
def list_products():
    query = Product.query

    search_term = (request.args.get("q") or "").strip()
    category_id = request.args.get("category_id")
    min_price = request.args.get("min_price")
    max_price = request.args.get("max_price")

    if search_term:
        like_pattern = f"%{search_term}%"
        query = query.filter(
            (Product.name.ilike(like_pattern))
            | (Product.description.ilike(like_pattern))
        )

    if category_id:
        try:
            query = query.filter(Product.category_id == int(category_id))
        except ValueError:
            return jsonify({"message": "category_id must be an integer"}), 400

    if min_price is not None:
        try:
            query = query.filter(Product.price >= float(min_price))
        except ValueError:
            return jsonify({"message": "min_price must be numeric"}), 400

    if max_price is not None:
        try:
            query = query.filter(Product.price <= float(max_price))
        except ValueError:
            return jsonify({"message": "max_price must be numeric"}), 400

    try:
        page = max(int(request.args.get("page", 1)), 1)
        per_page = min(max(int(request.args.get("per_page", 10)), 1), 100)
    except ValueError:
        return jsonify({"message": "page and per_page must be integers"}), 400

    pagination = query.order_by(Product.id.asc()).paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "data": [product_to_dict(product) for product in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total_items": pagination.total,
                "total_pages": pagination.pages,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
            },
            "filters": {
                "q": search_term or None,
                "category_id": category_id,
                "min_price": min_price,
                "max_price": max_price,
            },
        }
    ), 200


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify(product_to_dict(product)), 200


@app.route("/api/products/aggregations/by-category", methods=["GET"])
def products_aggregation_by_category():
    rows = (
        db.session.query(
            Category.id.label("category_id"),
            Category.name.label("category_name"),
            func.count(Product.id).label("product_count"),
            func.coalesce(func.min(Product.price), 0).label("min_price"),
            func.coalesce(func.max(Product.price), 0).label("max_price"),
            func.coalesce(func.avg(Product.price), 0).label("avg_price"),
        )
        .outerjoin(Product, Product.category_id == Category.id)
        .group_by(Category.id, Category.name)
        .order_by(Category.name.asc())
        .all()
    )

    return jsonify(
        [
            {
                "category_id": row.category_id,
                "category_name": row.category_name,
                "product_count": int(row.product_count),
                "min_price": float(row.min_price),
                "max_price": float(row.max_price),
                "avg_price": round(float(row.avg_price), 2),
            }
            for row in rows
        ]
    ), 200


@app.route("/api/carts", methods=["POST"])
def create_cart():
    data = request.get_json() or {}
    user_id = data.get("user_id")

    if user_id is None:
        return jsonify({"message": "user_id is required"}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    cart = Cart(user_id=user.id, status="open")
    db.session.add(cart)
    db.session.commit()

    return jsonify(cart_to_dict(cart)), 201


@app.route("/api/carts/<int:cart_id>/items", methods=["POST"])
def add_item_to_cart(cart_id):
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return jsonify({"message": "Cart not found"}), 404

    if cart.status != "open":
        return jsonify({"message": "Cannot modify a non-open cart"}), 400

    data = request.get_json() or {}
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    if product_id is None:
        return jsonify({"message": "product_id is required"}), 400

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        return jsonify({"message": "quantity must be an integer"}), 400

    if quantity <= 0:
        return jsonify({"message": "quantity must be greater than 0"}), 400

    product = db.session.get(Product, product_id)
    if not product:
        return jsonify({"message": "Product not found"}), 404

    existing_item = CartItem.query.filter_by(cart_id=cart.id, product_id=product.id).first()

    if existing_item:
        existing_item.quantity += quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price,
        )
        db.session.add(item)

    db.session.commit()
    return jsonify(cart_to_dict(cart)), 200


@app.route("/api/carts/<int:cart_id>", methods=["GET"])
def get_cart(cart_id):
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return jsonify({"message": "Cart not found"}), 404

    return jsonify(cart_to_dict(cart)), 200


if __name__ == "__main__":
    app.run(debug=True)
