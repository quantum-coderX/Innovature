from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required


share_bp = Blueprint('shares', __name__)


@share_bp.route('/notes/<int:note_id>/share', methods=['POST'])
@jwt_required()
def create_share_link(note_id):
    return jsonify({'message': 'Share link endpoint scaffolded', 'note_id': note_id}), 501


@share_bp.route('/notes/<int:note_id>/shares', methods=['GET'])
@jwt_required()
def list_share_links(note_id):
    return jsonify({'message': 'Share list endpoint scaffolded', 'note_id': note_id}), 501


@share_bp.route('/notes/<int:note_id>/shares/<int:share_id>', methods=['PATCH'])
@jwt_required()
def update_share_link(note_id, share_id):
    return jsonify({'message': 'Share update endpoint scaffolded', 'note_id': note_id, 'share_id': share_id}), 501


@share_bp.route('/notes/<int:note_id>/shares/<int:share_id>', methods=['DELETE'])
@jwt_required()
def delete_share_link(note_id, share_id):
    return jsonify({'message': 'Share delete endpoint scaffolded', 'note_id': note_id, 'share_id': share_id}), 501
