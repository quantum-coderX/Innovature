from database import db
from models import Note
from auth import get_current_user

def get_notes(user_id, skip=0, limit=100):
    return Note.query.filter_by(user_id=user_id).offset(skip).limit(limit).all()

def create_note(title, content, user_id):
    note = Note(title=title, content=content, user_id=user_id)
    db.session.add(note)
    db.session.commit()
    return note

def get_note(note_id, user_id):
    return Note.query.filter_by(id=note_id, user_id=user_id).first()

def update_note(note_id, title=None, content=None, user_id=None):
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if note:
        if title:
            note.title = title
        if content:
            note.content = content
        db.session.commit()
    return note

def delete_note(note_id, user_id):
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
    return note