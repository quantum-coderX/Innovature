from flask import Blueprint, jsonify
from crud import resolve_share_token
from serializers import error_response, serialize_public_note


public_bp = Blueprint('public', __name__)


@public_bp.route('/s/<string:token>', methods=['GET'])
def read_shared_note(token):
    link, status = resolve_share_token(token)

    if status == 'not_found':
        return error_response('Share link not found', 404)
    if status in ('revoked', 'expired'):
        return error_response('Share link is no longer active', 410)

    return jsonify(serialize_public_note(link)), 200
