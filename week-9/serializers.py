"""Serializers for converting models to JSON and vice versa"""


def error_response(message, status_code=400):
    """Generate error response tuple"""
    return {'error': message}, status_code


def serialize_category(category):
    """Serialize Category model to dict"""
    return {
        'id': category.id,
        'name': category.name,
        'description': category.description,
        'created_at': category.created_at.isoformat() if category.created_at else None,
        'updated_at': category.updated_at.isoformat() if category.updated_at else None,
    }


def serialize_categories(categories):
    """Serialize list of categories"""
    return [serialize_category(cat) for cat in categories]


def serialize_user(user):
    """Serialize User model to dict"""
    role_map = {
        1: 'seller',
        2: 'buyer',
    }

    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role_code': user.role,
        'role': role_map.get(user.role, 'unknown'),
        'phone': user.phone,
        'address': user.address,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat() if user.created_at else None,
        'updated_at': user.updated_at.isoformat() if user.updated_at else None,
    }


def serialize_users(users):
    """Serialize list of users"""
    return [serialize_user(user) for user in users]


def serialize_product(product):
    """Serialize Product model to dict"""
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': float(product.price) if product.price else 0.0,
        'stock': product.stock,
        'sku': product.sku,
        'seller_id': product.seller_id,
        'seller_name': product.seller.name if product.seller else None,
        'category_id': product.category_id,
        'category_name': product.category.name if product.category else None,
        'created_at': product.created_at.isoformat() if product.created_at else None,
        'updated_at': product.updated_at.isoformat() if product.updated_at else None,
    }


def serialize_products(products):
    """Serialize list of products"""
    return [serialize_product(product) for product in products]


def serialize_cart_item(item):
    """Serialize CartItem model to dict"""
    unit_price = float(item.unit_price) if item.unit_price else 0.0
    line_total = unit_price * item.quantity
    
    return {
        'id': item.id,
        'cart_id': item.cart_id,
        'product_id': item.product_id,
        'product_name': item.product.name if item.product else None,
        'quantity': item.quantity,
        'unit_price': unit_price,
        'line_total': round(line_total, 2),
        'created_at': item.created_at.isoformat() if item.created_at else None,
        'updated_at': item.updated_at.isoformat() if item.updated_at else None,
    }


def serialize_cart(cart):
    """Serialize Cart model to dict with totals"""
    items = [serialize_cart_item(item) for item in cart.items]
    total_amount = sum(item['line_total'] for item in items)
    items_count = sum(item['quantity'] for item in items)
    
    return {
        'id': cart.id,
        'user_id': cart.user_id,
        'user_name': cart.user.name if cart.user else None,
        'status': cart.status,
        'items': items,
        'items_count': items_count,
        'total_amount': round(total_amount, 2),
        'created_at': cart.created_at.isoformat() if cart.created_at else None,
        'updated_at': cart.updated_at.isoformat() if cart.updated_at else None,
    }


def serialize_carts(carts):
    """Serialize list of carts"""
    return [serialize_cart(cart) for cart in carts]


def serialize_aggregation_stats(stats):
    """Serialize aggregation statistics"""
    return {
        'total_products': stats.get('total_products', 0),
        'total_categories': stats.get('total_categories', 0),
        'total_users': stats.get('total_users', 0),
        'average_price': round(stats.get('average_price', 0.0), 2),
        'min_price': round(stats.get('min_price', 0.0), 2),
        'max_price': round(stats.get('max_price', 0.0), 2),
        'total_stock': stats.get('total_stock', 0),
        'total_carts': stats.get('total_carts', 0),
        'active_carts': stats.get('active_carts', 0),
        'products_by_category': stats.get('products_by_category', []),
    }


def success_response(data, message=None, status_code=200):
    """Generate success response tuple"""
    response = {'data': data}
    if message:
        response['message'] = message
    return response, status_code


def paginated_response(items, page, per_page, total, message=None):
    """Generate paginated response tuple"""
    response = {
        'data': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
            'has_next': page * per_page < total,
            'has_prev': page > 1,
        }
    }
    if message:
        response['message'] = message
    return response, 200
