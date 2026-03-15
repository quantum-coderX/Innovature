from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from auth import get_current_user
from crud import (
    create_share_link,
    delete_share_link,
    get_note_with_access_status,
    get_share_links_for_note,
    update_share_link,
)
from serializers import (
    error_response,
    parse_share_create_payload,
    parse_share_update_payload,
    serialize_share_link,
)


share_bp = Blueprint('shares', __name__)


def _note_access_error(status):
    if status == 'forbidden':
        return error_response('Forbidden', 403)
    return error_response('Note not found', 404)


@share_bp.route('/notes/<int:note_id>/share', methods=['POST'])
@jwt_required()
def create_share_link_route(note_id):
    user = get_current_user()
    _, access_status = get_note_with_access_status(note_id, user.id)
    if access_status != 'ok':
        return _note_access_error(access_status)

    payload, parse_error = parse_share_create_payload(request.get_json())
    if parse_error:
        return error_response(parse_error, 400)

    link = create_share_link(note_id, user.id, expires_at=payload['expires_at'])
    if link is None:
        return error_response('Note not found', 404)
    return jsonify(serialize_share_link(link)), 201


@share_bp.route('/notes/<int:note_id>/shares', methods=['GET'])
@jwt_required()
def list_share_links_route(note_id):
    user = get_current_user()
    _, access_status = get_note_with_access_status(note_id, user.id)
    if access_status != 'ok':
        return _note_access_error(access_status)

    links = get_share_links_for_note(note_id, user.id)
    if links is None:
        return error_response('Note not found', 404)
    return jsonify([serialize_share_link(l) for l in links]), 200


@share_bp.route('/notes/<int:note_id>/shares/<int:share_id>', methods=['PATCH'])
@jwt_required()
def update_share_link_route(note_id, share_id):
    user = get_current_user()
    _, access_status = get_note_with_access_status(note_id, user.id)
    if access_status != 'ok':
        return _note_access_error(access_status)

    updates, parse_error = parse_share_update_payload(request.get_json())
    if parse_error:
        return error_response(parse_error, 400)

    link = update_share_link(share_id, note_id, user.id, **updates)
    if link is None:
        return error_response('Share link not found', 404)
    return jsonify(serialize_share_link(link)), 200


@share_bp.route('/notes/<int:note_id>/shares/<int:share_id>', methods=['DELETE'])
@jwt_required()
def delete_share_link_route(note_id, share_id):
    user = get_current_user()
    _, access_status = get_note_with_access_status(note_id, user.id)
    if access_status != 'ok':
        return _note_access_error(access_status)

    link = delete_share_link(share_id, note_id, user.id)
    if link is None:
        return error_response('Share link not found', 404)
    return '', 204
