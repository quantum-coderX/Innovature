import secrets
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from database import db
from models import Note, Category, Tag, ShareLink


def get_categories():
    return Category.query.all()

def create_category(name):
    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return category

def get_category(category_id):
    return Category.query.get(category_id)

def update_category(category_id, name):
    category = Category.query.get(category_id)
    if category:
        category.name = name
        db.session.commit()
    return category

def delete_category(category_id):
    category = Category.query.get(category_id)
    if category:
        db.session.delete(category)
        db.session.commit()
    return category

# Tag CRUD
def get_tags():
    return Tag.query.all()

def create_tag(name):
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return tag

def get_tag(tag_id):
    return Tag.query.get(tag_id)

def update_tag(tag_id, name):
    tag = Tag.query.get(tag_id)
    if tag:
        tag.name = name
        db.session.commit()
    return tag

def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    if tag:
        db.session.delete(tag)
        db.session.commit()
    return tag

def get_notes(user_id, skip=0, limit=100, category_id=None, tag_id=None, search=None):
    query = Note.query.filter_by(user_id=user_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if tag_id:
        query = query.filter(Note.tags.any(id=tag_id))
    if search:
        query = query.filter(
            db.or_(
                Note.title.ilike(f'%{search}%'),
                Note.content.ilike(f'%{search}%')
            )
        )
    return query.offset(skip).limit(limit).all()

def create_note(title, content, user_id, category_id=None, tag_ids=None):
    note = Note(title=title, content=content, user_id=user_id, category_id=category_id)
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        note.tags = tags
    db.session.add(note)
    db.session.commit()
    return note

def get_note(note_id, user_id):
    return Note.query.filter_by(id=note_id, user_id=user_id).first()


def get_note_with_access_status(note_id, user_id):
    """Return (note, status) where status is 'ok', 'not_found', or 'forbidden'."""
    note = Note.query.get(note_id)
    if not note:
        return None, 'not_found'
    if note.user_id != user_id:
        return None, 'forbidden'
    return note, 'ok'

def update_note(note_id, title=None, content=None, user_id=None, category_id=None, tag_ids=None):
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if note:
        if title:
            note.title = title
        if content:
            note.content = content
        if category_id is not None:
            note.category_id = category_id
        if tag_ids is not None:
            tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
            note.tags = tags
        db.session.commit()
    return note

def delete_note(note_id, user_id):
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
    return note



def _generate_unique_token():
    for _ in range(10):
        token = secrets.token_urlsafe(24)
        if not ShareLink.query.filter_by(token=token).first():
            return token
    raise RuntimeError('Failed to generate a unique share token after 10 attempts')


def create_share_link(note_id, user_id, expires_at=None):
    """Create a new ShareLink for a note owned by user_id. Returns None if
    the note does not exist or does not belong to the user."""
    note = get_note(note_id, user_id)
    if not note:
        return None

    # Retry insert in case another request commits the same token first.
    for _ in range(10):
        token = _generate_unique_token()
        link = ShareLink(note_id=note_id, token=token, expires_at=expires_at)
        db.session.add(link)
        try:
            db.session.commit()
            return link
        except IntegrityError:
            db.session.rollback()

    raise RuntimeError('Failed to persist a unique share token after 10 attempts')


def get_share_links_for_note(note_id, user_id):
    """Return all ShareLinks for a note owned by user_id, or None if the
    note is not owned by the user."""
    if not get_note(note_id, user_id):
        return None
    return (
        ShareLink.query
        .filter_by(note_id=note_id)
        .order_by(ShareLink.created_at.desc())
        .all()
    )


def get_share_link(share_id, note_id, user_id):
    """Return a specific ShareLink only if the parent note is owned by
    user_id. Returns None otherwise."""
    if not get_note(note_id, user_id):
        return None
    return ShareLink.query.filter_by(id=share_id, note_id=note_id).first()


def update_share_link(share_id, note_id, user_id, **fields):
    """Update is_revoked and/or expires_at on a ShareLink owned by user_id.
    Pass the fields you want to change as keyword arguments.
    Returns None when the link is not found or not owned."""
    link = get_share_link(share_id, note_id, user_id)
    if not link:
        return None
    if 'expires_at' in fields:
        link.expires_at = fields['expires_at']
    if 'is_revoked' in fields:
        link.is_revoked = fields['is_revoked']
    db.session.commit()
    return link


def delete_share_link(share_id, note_id, user_id):
    """Delete a ShareLink owned by user_id. Returns the deleted link or
    None if not found."""
    link = get_share_link(share_id, note_id, user_id)
    if link:
        db.session.delete(link)
        db.session.commit()
    return link


def resolve_share_token(token):
    """Look up a token and validate it. On success increments access_count
    and updates last_accessed_at, then returns (share_link, 'ok').
    On failure returns (None, reason) where reason is one of
    'not_found', 'revoked', 'expired'."""
    link = ShareLink.query.filter_by(token=token).first()
    if not link:
        return None, 'not_found'
    if link.is_revoked:
        return None, 'revoked'
    if link.expires_at and link.expires_at < datetime.utcnow():
        return None, 'expired'

    # Use an atomic SQL update to avoid dropped increments under concurrency.
    now = datetime.utcnow()
    (
        db.session.query(ShareLink)
        .filter(ShareLink.id == link.id)
        .update(
            {
                ShareLink.access_count: ShareLink.access_count + 1,
                ShareLink.last_accessed_at: now,
            },
            synchronize_session=False,
        )
    )
    db.session.commit()
    db.session.refresh(link)
    return link, 'ok'