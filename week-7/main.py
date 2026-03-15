from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from database import db
from models import User, Note, Category, Tag, ShareLink
from config import Config
from routes import register_blueprints

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
jwt = JWTManager(app)

register_blueprints(app)

with app.app_context():
    db.create_all()

@app.route('/')
def health_check():
    return jsonify({'status': 'API is running', 'message': 'User Notes API with JWT auth'}), 200

if __name__ == '__main__':
    app.run(debug=True)