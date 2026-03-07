#!/usr/bin/env python3
"""
Database Inspection Script for User Notes API
Run this script to check the current state of the PostgreSQL database.
"""

from database import db
from models import User, Note
from config import Config
from flask import Flask
import os

def inspect_database():
    """Inspect and display database contents"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Check if we can connect to the database
    try:
        db.init_app(app)
        with app.app_context():
            print("🔍 Database Inspection Report")
            print("=" * 50)

            # Check users table
            users = User.query.all()
            print(f"\n👥 Users Table: {len(users)} total users")
            print("-" * 30)
            if users:
                for user in users:
                    note_count = len(user.notes)
                    print(f"ID: {user.id} | Username: {user.username} | Notes: {note_count}")
            else:
                print("No users found in database")

            # Check notes table
            notes = Note.query.all()
            print(f"\n📝 Notes Table: {len(notes)} total notes")
            print("-" * 30)
            if notes:
                for note in notes:
                    print(f"ID: {note.id} | Title: {note.title[:30]}{'...' if len(note.title) > 30 else ''}")
                    print(f"  User ID: {note.user_id} | Created: {note.created_at}")
                    print(f"  Content: {note.content[:50]}{'...' if len(note.content) > 50 else ''}")
                    print()
            else:
                print("No notes found in database")

            # Summary statistics
            print("\n📊 Summary Statistics")
            print("-" * 20)
            print(f"Total Users: {len(users)}")
            print(f"Total Notes: {len(notes)}")
            if users:
                avg_notes = len(notes) / len(users)
                print(".1f")
            print(f"Database Connection: ✅ Successful")

    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Make sure PostgreSQL container is running: docker-compose ps")
        print("2. Start database if needed: docker-compose up -d")
        print("3. Check environment variables in .env file")
        print("4. Verify Flask app has created tables by running the API first")

if __name__ == "__main__":
    inspect_database()