from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from routes import register_blueprints

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)
jwt = JWTManager(app)


# ==================== JWT Error Handlers ====================

@jwt.unauthorized_loader
def jwt_missing_token(reason):
    return jsonify({
        'error': 'Unauthorized',
        'message': reason,
        'hint': 'Send header: Authorization: Bearer <access_token>'
    }), 401


@jwt.invalid_token_loader
def jwt_invalid_token(reason):
    return jsonify({
        'error': 'Unauthorized',
        'message': f'Invalid token: {reason}',
        'hint': 'Re-login to get a valid access token'
    }), 401


@jwt.expired_token_loader
def jwt_expired_token(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Access token has expired',
        'hint': 'Login again to refresh your token'
    }), 401


@jwt.revoked_token_loader
def jwt_revoked_token(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Token has been revoked',
        'hint': 'Login again to get a new token'
    }), 401


@jwt.needs_fresh_token_loader
def jwt_needs_fresh_token(jwt_header, jwt_payload):
    return jsonify({
        'error': 'Unauthorized',
        'message': 'Fresh token required',
        'hint': 'Authenticate again and retry'
    }), 401


# Register all blueprints
register_blueprints(app)

# Create database tables (including new product_image table)
with app.app_context():
    db.create_all()

    # Ensure upload directories exist on startup
    upload_folder = app.config.get("UPLOAD_FOLDER", "static/uploads/products")
    thumb_folder  = app.config.get("THUMBNAIL_FOLDER", "static/uploads/thumbnails")
    os.makedirs(upload_folder, exist_ok=True)
    os.makedirs(thumb_folder, exist_ok=True)


# ==================== Static / Media File Serving ====================
# Serves files from  static/uploads/<path>
# Images:     http://localhost:5000/uploads/products/<filename>
# Thumbnails: http://localhost:5000/uploads/thumbnails/<filename>

@app.route('/uploads/<path:filename>')
def serve_upload(filename):
    """Serve uploaded product images and thumbnails."""
    return send_from_directory('static/uploads', filename)


# ==================== Error Handlers ====================

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(409)
def conflict(error):
    return jsonify({'error': 'Conflict'}), 409


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'error': 'Unauthorized'}), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Forbidden'}), 403


# ==================== Health Check ====================

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'Week 10 E-commerce API',
        'version': '2.0.0',
        'features': {
            'products':      'Public product browsing with search, filters (price/category), pagination',
            'product_images': 'Multiple images per product with automatic 300×300 thumbnail generation',
            'roles':         'Seller/Buyer roles (only sellers can manage products/images)',
            'categories':    'Product organization and management',
            'auth':          'JWT registration/login/profile validation',
            'carts':         'Shopping cart with checkout stock deduction',
            'aggregations':  'Analytics and statistics endpoints',
            'static_files':  'Images served at /uploads/products/ and /uploads/thumbnails/',
        }
    }), 200


# ==================== Entry Point ====================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
