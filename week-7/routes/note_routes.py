from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from auth import get_current_user
from crud import (
    create_category,
    create_note,
    create_tag,
    delete_category,
    delete_note,
    delete_tag,
    get_categories,
    get_category,
    get_note,
    get_notes,
    get_tag,
    get_tags,
    update_category,
    update_note,
    update_tag,
)


note_bp = Blueprint('notes', __name__)


def error(msg, code):
    return jsonify({'error': msg}), code


def note_dict(note):
    return {
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat(),
        'category': {'id': note.category.id, 'name': note.category.name} if note.category else None,
        'tags': [{'id': t.id, 'name': t.name} for t in note.tags],
    }


def category_dict(cat):
    return {
        'id': cat.id,
        'name': cat.name,
        'created_at': cat.created_at.isoformat(),
        'updated_at': cat.updated_at.isoformat(),
    }


def tag_dict(tag):
    return {
        'id': tag.id,
        'name': tag.name,
        'created_at': tag.created_at.isoformat(),
        'updated_at': tag.updated_at.isoformat(),
    }


@note_bp.route('/categories', methods=['GET'])
@jwt_required()
def read_categories():
    try:
        return jsonify([category_dict(c) for c in get_categories()]), 200
    except Exception:
        return error('Internal server error', 500)


@note_bp.route('/categories', methods=['POST'])
@jwt_required()
def create_user_category():
    data = request.get_json()
    if not data:
        return error('Bad request', 400)

    name = data.get('name', '').strip()
    if not name or len(name) > 100:
        return error('Bad request', 400)

    try:
        return jsonify(category_dict(create_category(name))), 201
    except Exception as e:
        if 'unique constraint' in str(e).lower():
            return error('Conflict', 409)
        return error('Internal server error', 500)


@note_bp.route('/categories/<int:category_id>', methods=['GET'])
@jwt_required()
def read_category(category_id):
    cat = get_category(category_id)
    if not cat:
        return error('Not found', 404)
    return jsonify(category_dict(cat)), 200


@note_bp.route('/categories/<int:category_id>', methods=['PATCH'])
@jwt_required()
def update_user_category(category_id):
    data = request.get_json()
    if not data:
        return error('Bad request', 400)

    name = data.get('name')
    if name is not None:
        name = name.strip()
        if len(name) > 100:
            return error('Bad request', 400)

    try:
        cat = update_category(category_id, name)
        if not cat:
            return error('Not found', 404)
        return jsonify(category_dict(cat)), 200
    except Exception as e:
        if 'unique constraint' in str(e).lower():
            return error('Conflict', 409)
        return error('Internal server error', 500)


@note_bp.route('/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
def delete_user_category(category_id):
    try:
        if not delete_category(category_id):
            return error('Not found', 404)
        return '', 204
    except Exception:
        return error('Internal server error', 500)


@note_bp.route('/tags', methods=['GET'])
@jwt_required()
def read_tags():
    try:
        return jsonify([tag_dict(t) for t in get_tags()]), 200
    except Exception:
        return error('Internal server error', 500)


@note_bp.route('/tags', methods=['POST'])
@jwt_required()
def create_user_tag():
    data = request.get_json()
    if not data:
        return error('Bad request', 400)

    name = data.get('name', '').strip()
    if not name or len(name) > 50:
        return error('Bad request', 400)

    try:
        return jsonify(tag_dict(create_tag(name))), 201
    except Exception as e:
        if 'unique constraint' in str(e).lower():
            return error('Conflict', 409)
        return error('Internal server error', 500)


@note_bp.route('/tags/<int:tag_id>', methods=['GET'])
@jwt_required()
def read_tag(tag_id):
    t = get_tag(tag_id)
    if not t:
        return error('Not found', 404)
    return jsonify(tag_dict(t)), 200


@note_bp.route('/tags/<int:tag_id>', methods=['PATCH'])
@jwt_required()
def update_user_tag(tag_id):
    data = request.get_json()
    if not data:
        return error('Bad request', 400)

    name = data.get('name')
    if name is not None:
        name = name.strip()
        if len(name) > 50:
            return error('Bad request', 400)

    try:
        t = update_tag(tag_id, name)
        if not t:
            return error('Not found', 404)
        return jsonify(tag_dict(t)), 200
    except Exception as e:
        if 'unique constraint' in str(e).lower():
            return error('Conflict', 409)
        return error('Internal server error', 500)


@note_bp.route('/tags/<int:tag_id>', methods=['DELETE'])
@jwt_required()
def delete_user_tag(tag_id):
    try:
        if not delete_tag(tag_id):
            return error('Not found', 404)
        return '', 204
    except Exception:
        return error('Internal server error', 500)


@note_bp.route('/notes', methods=['GET'])
@jwt_required()
def read_notes():
    user = get_current_user()
    try:
        category_id = request.args.get('category', type=int)
        tag_id = request.args.get('tag', type=int)
        search = request.args.get('search', '').strip()
        notes = get_notes(user.id, category_id=category_id, tag_id=tag_id, search=search)
        return jsonify([note_dict(n) for n in notes]), 200
    except Exception:
        return error('Internal server error', 500)


@note_bp.route('/notes', methods=['POST'])
@jwt_required()
def create_user_note():
    user = get_current_user()
    data = request.get_json()
    if not data:
        return error('Bad request', 400)

    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    category_id = data.get('category_id')
    tag_ids = data.get('tag_ids', [])

    if not title or not content:
        return error('Bad request', 400)
    if len(title) > 200 or len(content) > 10000:
        return error('Bad request', 400)
    if category_id is not None and not get_category(category_id):
        return error('Bad request', 400)
    if tag_ids and not all(get_tag(tid) for tid in tag_ids):
        return error('Bad request', 400)

    try:
        note = create_note(title, content, user.id, category_id, tag_ids)
        return jsonify(note_dict(note)), 201
    except Exception:
        return error('Internal server error', 500)


@note_bp.route('/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def read_note(note_id):
    user = get_current_user()
    note = get_note(note_id, user.id)
    if not note:
        return error('Not found', 404)
    return jsonify(note_dict(note)), 200


@note_bp.route('/notes/<int:note_id>', methods=['PATCH'])
@jwt_required()
def update_user_note(note_id):
    user = get_current_user()
    data = request.get_json()
    if not data:
        return error('Bad request', 400)

    title = data.get('title')
    if title is not None:
        title = title.strip()
        if len(title) > 200:
            return error('Bad request', 400)

    content = data.get('content')
    if content is not None:
        content = content.strip()
        if len(content) > 10000:
            return error('Bad request', 400)

    category_id = data.get('category_id')
    if category_id is not None and not get_category(category_id):
        return error('Bad request', 400)

    tag_ids = data.get('tag_ids')
    if tag_ids is not None and not all(get_tag(tid) for tid in tag_ids):
        return error('Bad request', 400)

    try:
        note = update_note(note_id, title, content, user.id, category_id, tag_ids)
        if not note:
            return error('Not found', 404)
        return jsonify(note_dict(note)), 200
    except Exception:
        return error('Internal server error', 500)


@note_bp.route('/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_user_note(note_id):
    user = get_current_user()
    try:
        if not delete_note(note_id, user.id):
            return error('Not found', 404)
        return '', 204
    except Exception:
        return error('Internal server error', 500)
