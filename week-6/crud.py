from database import db
from models import Note, Category, Tag
from auth import get_current_user

# Category CRUD
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

# Note CRUD with categories and tags
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