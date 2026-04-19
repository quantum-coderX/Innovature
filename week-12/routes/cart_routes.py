"""Cart routes for shopping cart management"""

from flask import Blueprint, request
from database import db
from models import Cart, CartItem, Product
from serializers import serialize_cart, serialize_carts, error_response, success_response, paginated_response
from auth import jwt_required_active_user, get_current_user
from crud import checkout_cart

cart_bp = Blueprint('carts', __name__, url_prefix='/api/carts')


@cart_bp.route('', methods=['POST'])
@jwt_required_active_user
def create_cart():
    """Create a new cart for a user"""
    current_user = get_current_user()

    cart = Cart(user_id=current_user.id, status='open')

    db.session.add(cart)
    db.session.commit()

    return success_response(serialize_cart(cart), 'Cart created successfully', 201)


@cart_bp.route('', methods=['GET'])
@jwt_required_active_user
def list_carts():
    """Get all carts with pagination"""
    current_user = get_current_user()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status')

    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:
        per_page = 10

    query = Cart.query.filter_by(user_id=current_user.id)

    if status:
        query = query.filter_by(status=status)

    total = query.count()

    carts = query.order_by(Cart.created_at.desc()).offset((page - 1) * per_page).limit(per_page).all()

    return paginated_response(serialize_carts(carts), page, per_page, total)


@cart_bp.route('/<int:cart_id>', methods=['GET'])
@jwt_required_active_user
def get_cart(cart_id):
    """Get a specific cart by ID"""
    current_user = get_current_user()
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return error_response('Cart not found', 404)
    if cart.user_id != current_user.id:
        return error_response('Forbidden: not your cart', 403)
    return success_response(serialize_cart(cart))


@cart_bp.route('/<int:cart_id>/items', methods=['POST'])
@jwt_required_active_user
def add_to_cart(cart_id):
    """Add a product to cart"""
    current_user = get_current_user()
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return error_response('Cart not found', 404)
    if cart.user_id != current_user.id:
        return error_response('Forbidden: not your cart', 403)
    if cart.status != 'open':
        return error_response(f'Cannot add items to a {cart.status} cart', 400)
    data = request.get_json() or {}

    product_id = data.get('product_id')
    if not product_id:
        return error_response('product_id is required')

    product = Product.query.get(product_id)
    if not product:
        return error_response(f'Product with ID {product_id} not found')

    if product.stock <= 0:
        return error_response('Product is out of stock')

    try:
        quantity = int(data.get('quantity', 1))
        if quantity < 1:
            return error_response('Quantity must be at least 1')
        if quantity > product.stock:
            return error_response(f'Insufficient stock. Available: {product.stock}')
    except (ValueError, TypeError):
        return error_response('Invalid quantity format')

    existing_item = CartItem.query.filter_by(
        cart_id=cart_id,
        product_id=product_id
    ).first()

    if existing_item:
        new_quantity = existing_item.quantity + quantity
        if new_quantity > product.stock:
            return error_response(f'Insufficient stock. Available: {product.stock}')
        existing_item.quantity = new_quantity
    else:
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=product.price
        )
        db.session.add(cart_item)

    db.session.commit()

    return success_response(serialize_cart(cart), 'Item added to cart successfully', 201)


@cart_bp.route('/<int:cart_id>/items/<int:item_id>', methods=['PUT'])
@jwt_required_active_user
def update_cart_item(cart_id, item_id):
    """Update quantity of a cart item"""
    current_user = get_current_user()
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return error_response('Cart not found', 404)
    if cart.user_id != current_user.id:
        return error_response('Forbidden: not your cart', 403)

    cart_item = CartItem.query.filter_by(
        id=item_id,
        cart_id=cart_id
    ).first_or_404('Cart item not found')

    data = request.get_json() or {}

    try:
        quantity = int(data.get('quantity', 1))
        if quantity < 1:
            return error_response('Quantity must be at least 1')
        if quantity > cart_item.product.stock:
            return error_response(f'Insufficient stock. Available: {cart_item.product.stock}')
    except (ValueError, TypeError):
        return error_response('Invalid quantity format')

    cart_item.quantity = quantity
    db.session.commit()

    return success_response(serialize_cart(cart), 'Cart item updated successfully')


@cart_bp.route('/<int:cart_id>/items/<int:item_id>', methods=['DELETE'])
@jwt_required_active_user
def remove_from_cart(cart_id, item_id):
    """Remove an item from cart"""
    current_user = get_current_user()
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return error_response('Cart not found', 404)
    if cart.user_id != current_user.id:
        return error_response('Forbidden: not your cart', 403)

    cart_item = CartItem.query.filter_by(
        id=item_id,
        cart_id=cart_id
    ).first_or_404('Cart item not found')

    db.session.delete(cart_item)
    db.session.commit()

    return success_response(serialize_cart(cart), 'Item removed from cart')


@cart_bp.route('/<int:cart_id>/clear', methods=['POST'])
@jwt_required_active_user
def clear_cart(cart_id):
    """Clear all items from a cart"""
    current_user = get_current_user()
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return error_response('Cart not found', 404)
    if cart.user_id != current_user.id:
        return error_response('Forbidden: not your cart', 403)

    CartItem.query.filter_by(cart_id=cart_id).delete()
    db.session.commit()

    return success_response(serialize_cart(cart), 'Cart cleared successfully')


@cart_bp.route('/<int:cart_id>/status', methods=['PUT'])
@jwt_required_active_user
def update_cart_status(cart_id):
    """Update cart status"""
    current_user = get_current_user()
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return error_response('Cart not found', 404)
    if cart.user_id != current_user.id:
        return error_response('Forbidden: not your cart', 403)
    data = request.get_json() or {}

    status = (data.get('status') or '').strip().lower()
    valid_statuses = ['open', 'checkout', 'completed', 'abandoned']

    if not status or status not in valid_statuses:
        return error_response(f'Invalid status. Must be one of: {", ".join(valid_statuses)}')

    if status == 'completed' and cart.status != 'completed':
        try:
            checkout_cart(cart)
        except ValueError as exc:
            return error_response(str(exc))

    cart.status = status
    db.session.commit()

    return success_response(serialize_cart(cart), 'Cart status updated successfully')


@cart_bp.route('/<int:cart_id>', methods=['DELETE'])
@jwt_required_active_user
def delete_cart(cart_id):
    """Delete a cart"""
    current_user = get_current_user()
    cart = db.session.get(Cart, cart_id)
    if not cart:
        return error_response('Cart not found', 404)
    if cart.user_id != current_user.id:
        return error_response('Forbidden: not your cart', 403)

    db.session.delete(cart)
    db.session.commit()

    return {'message': 'Cart deleted successfully'}, 200
