from datetime import datetime, timezone
from flask import jsonify, url_for


def error_response(message, status_code):
    return jsonify({'error': message}), status_code


def serialize_note(note):
    return {
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat(),
        'category': {'id': note.category.id, 'name': note.category.name} if note.category else None,
        'tags': [{'id': t.id, 'name': t.name} for t in note.tags],
    }


def serialize_category(category):
    return {
        'id': category.id,
        'name': category.name,
        'created_at': category.created_at.isoformat(),
        'updated_at': category.updated_at.isoformat(),
    }


def serialize_tag(tag):
    return {
        'id': tag.id,
        'name': tag.name,
        'created_at': tag.created_at.isoformat(),
        'updated_at': tag.updated_at.isoformat(),
    }


def serialize_share_link(link):
    return {
        'id': link.id,
        'note_id': link.note_id,
        'token': link.token,
        'share_url': url_for('public.read_shared_note', token=link.token, _external=True),
        'expires_at': link.expires_at.isoformat() if link.expires_at else None,
        'access_count': link.access_count,
        'created_at': link.created_at.isoformat(),
        'last_accessed_at': link.last_accessed_at.isoformat() if link.last_accessed_at else None,
        'is_revoked': link.is_revoked,
    }


def serialize_public_note(link):
    note = link.note
    return {
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'created_at': note.created_at.isoformat(),
        'category': {'id': note.category.id, 'name': note.category.name} if note.category else None,
        'tags': [{'id': t.id, 'name': t.name} for t in note.tags],
        'share': {
            'access_count': link.access_count,
            'expires_at': link.expires_at.isoformat() if link.expires_at else None,
        },
    }


def _parse_iso_to_utc_naive(value):
    try:
        dt = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return dt
    except (ValueError, AttributeError):
        raise ValueError('Invalid datetime format')


def parse_share_create_payload(data):
    data = data or {}
    expires_at = None
    if 'expires_at' in data:
        if data['expires_at'] is None:
            expires_at = None
        else:
            try:
                expires_at = _parse_iso_to_utc_naive(data['expires_at'])
            except ValueError:
                return None, 'Invalid expires_at: use ISO-8601 format e.g. 2026-04-01T12:00:00Z'
            if expires_at <= datetime.utcnow():
                return None, 'expires_at must be a future datetime'
    return {'expires_at': expires_at}, None


def parse_share_update_payload(data):
    if not data:
        return None, 'Bad request'

    updates = {}

    if 'expires_at' in data:
        if data['expires_at'] is None:
            updates['expires_at'] = None
        else:
            try:
                updates['expires_at'] = _parse_iso_to_utc_naive(data['expires_at'])
            except ValueError:
                return None, 'Invalid expires_at: use ISO-8601 format e.g. 2026-04-01T12:00:00Z'
            if updates['expires_at'] <= datetime.utcnow():
                return None, 'expires_at must be a future datetime'

    if 'is_revoked' in data:
        if not isinstance(data['is_revoked'], bool):
            return None, 'is_revoked must be a boolean'
        updates['is_revoked'] = data['is_revoked']

    if not updates:
        return None, 'No valid fields to update'

    return updates, None
