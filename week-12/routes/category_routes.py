"""Category routes for managing product categories"""

from flask import Blueprint, request
from database import db
from models import Category, Product
from serializers import (
    serialize_category, serialize_categories,
    error_response, success_response, serialize_products
)
from auth import seller_required

category_bp = Blueprint('categories', __name__, url_prefix='/api/categories')


@category_bp.route('', methods=['POST'])
@seller_required
def create_category():
    """Create a new product category"""
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()

    if not name:
        return error_response('Category name is required')

    if len(name) < 2 or len(name) > 100:
        return error_response('Category name must be between 2 and 100 characters')

    if Category.query.filter_by(name=name).first():
        return error_response('Category already exists')

    category = Category(
        name=name,
        description=data.get('description', '').strip() or None
    )

    db.session.add(category)
    db.session.commit()

    return success_response(serialize_category(category), 'Category created successfully', 201)


@category_bp.route('', methods=['GET'])
def list_categories():
    """Get all categories (with optional pagination)"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10

    query = Category.query.order_by(Category.name.asc())
    total = query.count()
    categories = query.offset((page - 1) * per_page).limit(per_page).all()

    response = {
        'data': serialize_categories(categories),
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page,
            'has_next': page * per_page < total,
            'has_prev': page > 1,
        }
    }

    return response, 200


@category_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a specific category by ID with its products"""
    category = db.session.get(Category, category_id)
    if not category:
        return error_response('Category not found', 404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10

    products_query = Product.query.filter(
        Product.category_id == category_id,
        Product.stock > 0
    ).order_by(Product.name.asc())
    total_products = products_query.count()
    products = products_query.offset((page - 1) * per_page).limit(per_page).all()

    response = serialize_category(category)
    response['products'] = serialize_products(products)
    response['products_count'] = total_products
    response['pagination'] = {
        'page': page,
        'per_page': per_page,
        'total': total_products,
        'total_pages': (total_products + per_page - 1) // per_page,
        'has_next': page * per_page < total_products,
        'has_prev': page > 1,
    }

    return success_response(response)


@category_bp.route('/<int:category_id>', methods=['PUT'])
@seller_required
def update_category(category_id):
    """Update a category"""
    category = db.session.get(Category, category_id)
    if not category:
        return error_response('Category not found', 404)
    data = request.get_json() or {}

    if 'name' in data:
        name = (data.get('name') or '').strip()
        if not name:
            return error_response('Category name cannot be empty')
        if len(name) > 100:
            return error_response('Category name must be at most 100 characters')

        existing = Category.query.filter_by(name=name).filter(Category.id != category_id).first()
        if existing:
            return error_response('Category with this name already exists')

        category.name = name

    if 'description' in data:
        category.description = (data.get('description') or '').strip() or None

    db.session.commit()

    return success_response(serialize_category(category), 'Category updated successfully')


@category_bp.route('/<int:category_id>', methods=['DELETE'])
@seller_required
def delete_category(category_id):
    """Delete a category"""
    category = db.session.get(Category, category_id)
    if not category:
        return error_response('Category not found', 404)

    if category.products:
        return error_response(
            'Cannot delete category with existing products. Remove or reassign its products first.',
            409
        )

    db.session.delete(category)
    db.session.commit()

    return {'message': 'Category deleted successfully'}, 200
