from .auth_routes import auth_bp
from .note_routes import note_bp
from .share_routes import share_bp
from .public_routes import public_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(note_bp)
    app.register_blueprint(share_bp)
    app.register_blueprint(public_bp)
