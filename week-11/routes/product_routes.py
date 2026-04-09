"""Product routes with search, filters, and pagination"""

from flask import Blueprint, request
from sqlalchemy import func, and_
from database import db
from models import Product, Category
from serializers import serialize_product, serialize_products, error_response, success_response, paginated_response
from auth import seller_required, get_current_user
from crud import get_public_products_query, create_product_for_seller

product_bp = Blueprint('products', __name__, url_prefix='/api/products')


@product_bp.route('', methods=['POST'])
@seller_required
def create_product():
    """Create a new product"""
    data = request.get_json() or {}
    current_user = get_current_user()

    name = (data.get('name') or '').strip()
    if not name:
        return error_response('Product name is required')

    try:
        price = float(data.get('price', 0))
        if price < 0:
            return error_response('Price must be a positive number')
    except (ValueError, TypeError):
        return error_response('Invalid price format')

    try:
        stock = int(data.get('stock', 0))
        if stock < 0:
            return error_response('Stock must be non-negative')
    except (ValueError, TypeError):
        return error_response('Invalid stock format')

    category_id = data.get('category_id')
    if not category_id:
        return error_response('Category ID is required')

    category = Category.query.get(category_id)
    if not category:
        return error_response(f'Category with ID {category_id} not found')

    sku = data.get('sku', '').strip() or None
    if sku and Product.query.filter_by(sku=sku).first():
        return error_response('Product with this SKU already exists')

    product = create_product_for_seller(
        seller_id=current_user.id,
        name=name,
        description=data.get('description', '').strip() or None,
        price=price,
        stock=stock,
        sku=sku,
        category_id=category_id,
    )
    db.session.commit()

    return success_response(serialize_product(product), 'Product created successfully', 201)


@product_bp.route('', methods=['GET'])
def list_products():
    """
    List products with search, filters, and pagination

    Query Parameters:
    - search: Search by product name or description
    - category_id: Filter by category ID
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - in_stock: Filter only in-stock items (true/false)
    - page: Page number (default: 1)
    - per_page: Items per page (default: 10, max: 100)
    - sort_by: Sort field (price, name, created_at)
    - sort_order: Sort order (asc, desc)
    """

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10

    query = get_public_products_query()

    search = (request.args.get('search') or '').strip().lower()
    if search and len(search) >= 2:
        query = query.filter(
            db.or_(
                func.lower(Product.name).contains(search),
                func.lower(Product.description).contains(search)
            )
        )

    category_id = request.args.get('category_id', type=int)
    if category_id:
        category = Category.query.get(category_id)
        if not category:
            return error_response(f'Category with ID {category_id} not found')
        query = query.filter_by(category_id=category_id)

    min_price = request.args.get('min_price', type=float)
    if min_price is not None:
        if min_price < 0:
            return error_response('min_price must be non-negative')
        query = query.filter(Product.price >= min_price)

    max_price = request.args.get('max_price', type=float)
    if max_price is not None:
        if max_price < 0:
            return error_response('max_price must be non-negative')
        query = query.filter(Product.price <= max_price)

    in_stock = (request.args.get('in_stock', type=str) or '').lower()
    if in_stock in ['true', '1', 'yes']:
        query = query.filter(Product.stock > 0)

    total = query.count()

    sort_by = request.args.get('sort_by', 'created_at').lower()
    sort_order = request.args.get('sort_order', 'desc').lower()

    if sort_by == 'price':
        sort_column = Product.price
    elif sort_by == 'name':
        sort_column = Product.name
    else:
        sort_column = Product.created_at

    if sort_order == 'asc':
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    products = query.offset((page - 1) * per_page).limit(per_page).all()

    return paginated_response(serialize_products(products), page, per_page, total)


@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID (includes images)"""
    product = db.session.get(Product, product_id)
    if not product:
        return error_response('Product not found', 404)
    if product.stock <= 0:
        return error_response('Product not available', 404)
    return success_response(serialize_product(product))   # include_images=True by default


@product_bp.route('/<int:product_id>', methods=['PUT'])
@seller_required
def update_product(product_id):
    """Update a product"""
    current_user = get_current_user()
    product = db.session.get(Product, product_id)
    if not product:
        return error_response('Product not found', 404)
    if product.seller_id != current_user.id:
        return error_response('Forbidden: you can only update your own products', 403)
    data = request.get_json() or {}

    if 'name' in data:
        name = (data.get('name') or '').strip()
        if not name:
            return error_response('Product name cannot be empty')
        product.name = name

    if 'description' in data:
        product.description = (data.get('description') or '').strip() or None

    if 'price' in data:
        try:
            price = float(data.get('price'))
            if price < 0:
                return error_response('Price must be non-negative')
            product.price = price
        except (ValueError, TypeError):
            return error_response('Invalid price format')

    if 'stock' in data:
        try:
            stock = int(data.get('stock'))
            if stock < 0:
                return error_response('Stock must be non-negative')
            product.stock = stock
        except (ValueError, TypeError):
            return error_response('Invalid stock format')

    if 'category_id' in data:
        category_id = data.get('category_id')
        category = Category.query.get(category_id)
        if not category:
            return error_response(f'Category with ID {category_id} not found')
        product.category_id = category_id

    if 'sku' in data:
        sku = (data.get('sku') or '').strip() or None
        if sku:
            existing = Product.query.filter(
                and_(Product.sku == sku, Product.id != product_id)
            ).first()
            if existing:
                return error_response('Product with this SKU already exists')
        product.sku = sku

    db.session.commit()

    return success_response(serialize_product(product), 'Product updated successfully')


@product_bp.route('/<int:product_id>', methods=['DELETE'])
@seller_required
def delete_product(product_id):
    """Delete a product"""
    current_user = get_current_user()
    product = db.session.get(Product, product_id)
    if not product:
        return error_response('Product not found', 404)
    if product.seller_id != current_user.id:
        return error_response('Forbidden: you can only delete your own products', 403)

    db.session.delete(product)
    db.session.commit()

    return {'message': 'Product deleted successfully'}, 200
