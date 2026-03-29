"""Aggregation routes for analytics and statistics"""

from flask import Blueprint
from sqlalchemy import func
from database import db
from models import Product, Category, User, Cart, CartItem
from serializers import serialize_aggregation_stats, success_response

aggregation_bp = Blueprint('aggregations', __name__, url_prefix='/api/aggregations')


@aggregation_bp.route('/stats', methods=['GET'])
def get_aggregation_stats():
    """
    Get comprehensive aggregation statistics
    
    Returns:
    - Total products and categories
    - Average, min, max prices
    - Stock information
    - Cart statistics
    - Products by category breakdown
    """
    
    try:
        # Count totals
        total_products = Product.query.count()
        total_categories = Category.query.count()
        total_users = User.query.count()
        total_carts = Cart.query.count()
        active_carts = Cart.query.filter_by(status='open').count()
        total_stock = int(db.session.query(func.sum(Product.stock)).scalar() or 0)
        
        # Price statistics
        price_stats = db.session.query(
            func.avg(Product.price).label('avg_price'),
            func.min(Product.price).label('min_price'),
            func.max(Product.price).label('max_price')
        ).first()
        
        avg_price = float(price_stats.avg_price) if price_stats.avg_price else 0.0
        min_price = float(price_stats.min_price) if price_stats.min_price else 0.0
        max_price = float(price_stats.max_price) if price_stats.max_price else 0.0
        
        # Products by category
        category_stats = db.session.query(
            Category.id,
            Category.name,
            func.count(Product.id).label('product_count')
        ).outerjoin(Product).group_by(Category.id, Category.name).all()
        
        products_by_category = [
            {
                'category_id': stat[0],
                'category_name': stat[1],
                'product_count': stat[2]
            }
            for stat in category_stats
        ]
        
        # Cart statistics
        total_cart_items = CartItem.query.count()
        avg_cart_value = 0.0
        
        cart_values = db.session.query(
            func.sum(CartItem.unit_price * CartItem.quantity).label('cart_total')
        ).group_by(CartItem.cart_id).all()
        
        if cart_values and len(cart_values) > 0:
            total_cart_value = sum(float(cv[0]) if cv[0] else 0.0 for cv in cart_values)
            avg_cart_value = total_cart_value / len(cart_values) if len(cart_values) > 0 else 0.0
        
        stats = {
            'total_products': total_products,
            'total_categories': total_categories,
            'total_users': total_users,
            'average_price': avg_price,
            'min_price': min_price,
            'max_price': max_price,
            'total_stock': total_stock,
            'total_carts': total_carts,
            'active_carts': active_carts,
            'total_cart_items': total_cart_items,
            'average_cart_value': round(avg_cart_value, 2),
            'products_by_category': products_by_category,
        }
        
        return success_response(serialize_aggregation_stats(stats))
    
    except Exception as e:
        return {'error': f'Failed to fetch statistics: {str(e)}'}, 500


@aggregation_bp.route('/category-breakdown', methods=['GET'])
def get_category_breakdown():
    """Get detailed breakdown by category with product count and price ranges"""
    
    try:
        categories_data = db.session.query(
            Category.id,
            Category.name,
            func.count(Product.id).label('product_count'),
            func.avg(Product.price).label('avg_price'),
            func.min(Product.price).label('min_price'),
            func.max(Product.price).label('max_price'),
            func.sum(Product.stock).label('total_stock')
        ).outerjoin(Product).group_by(Category.id, Category.name).all()
        
        breakdown = [
            {
                'category_id': cat[0],
                'category_name': cat[1],
                'product_count': cat[2],
                'average_price': round(float(cat[3]) if cat[3] else 0.0, 2),
                'min_price': round(float(cat[4]) if cat[4] else 0.0, 2),
                'max_price': round(float(cat[5]) if cat[5] else 0.0, 2),
                'total_stock': cat[6] or 0,
            }
            for cat in categories_data
        ]
        
        return success_response({
            'category_breakdown': breakdown,
            'total_categories': len(breakdown)
        })
    
    except Exception as e:
        return {'error': f'Failed to fetch category breakdown: {str(e)}'}, 500


@aggregation_bp.route('/price-distribution', methods=['GET'])
def get_price_distribution():
    """Get product count distribution by price ranges"""
    
    try:
        # Define price ranges
        ranges = [
            (0, 50, '0-50'),
            (50, 100, '50-100'),
            (100, 250, '100-250'),
            (250, 500, '250-500'),
            (500, 1000, '500-1000'),
            (1000, float('inf'), '1000+')
        ]
        
        distribution = []
        
        for min_p, max_p, label in ranges:
            if max_p == float('inf'):
                count = Product.query.filter(Product.price >= min_p).count()
            else:
                count = Product.query.filter(
                    Product.price >= min_p,
                    Product.price < max_p
                ).count()
            
            distribution.append({
                'price_range': label,
                'count': count
            })
        
        return success_response({
            'price_distribution': distribution
        })
    
    except Exception as e:
        return {'error': f'Failed to fetch price distribution: {str(e)}'}, 500


@aggregation_bp.route('/cart-analytics', methods=['GET'])
def get_cart_analytics():
    """Get detailed cart analytics"""
    
    try:
        # Cart by status
        status_breakdown = db.session.query(
            Cart.status,
            func.count(Cart.id).label('count')
        ).group_by(Cart.status).all()
        
        status_data = [
            {'status': status, 'count': count}
            for status, count in status_breakdown
        ]
        
        # Average items per cart
        items_per_cart_subquery = db.session.query(
            CartItem.cart_id,
            func.sum(CartItem.quantity).label('items_count')
        ).group_by(CartItem.cart_id).subquery()

        avg_items_per_cart = db.session.query(
            func.avg(items_per_cart_subquery.c.items_count)
        ).scalar() or 0.0
        
        # Most popular products in carts
        popular_products = db.session.query(
            CartItem.product_id,
            Product.name,
            func.sum(CartItem.quantity).label('total_quantity'),
            func.count(func.distinct(CartItem.cart_id)).label('cart_count')
        ).join(Product).group_by(
            CartItem.product_id, Product.name
        ).order_by(
            func.sum(CartItem.quantity).desc()
        ).limit(10).all()
        
        popular_data = [
            {
                'product_id': prod[0],
                'product_name': prod[1],
                'total_quantity': prod[2],
                'in_carts': prod[3]
            }
            for prod in popular_products
        ]
        
        return success_response({
            'carts_by_status': status_data,
            'average_items_per_cart': round(float(avg_items_per_cart), 2),
            'popular_products': popular_data
        })
    
    except Exception as e:
        return {'error': f'Failed to fetch cart analytics: {str(e)}'}, 500
