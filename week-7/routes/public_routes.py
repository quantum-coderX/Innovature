from flask import Blueprint, jsonify


public_bp = Blueprint('public', __name__)


@public_bp.route('/s/<string:token>', methods=['GET'])
def read_shared_note(token):
    return jsonify({'message': 'Public share endpoint scaffolded', 'token': token}), 501
