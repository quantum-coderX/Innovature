"""Routes package for E-commerce API"""

from .product_routes import product_bp
from .category_routes import category_bp
from .auth_routes import auth_bp
from .cart_routes import cart_bp
from .aggregation_routes import aggregation_bp
from .image_routes import image_bp          # Week 10


def register_blueprints(app):
    """Register all blueprints with the Flask app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(aggregation_bp)
    app.register_blueprint(image_bp)        # Week 10
