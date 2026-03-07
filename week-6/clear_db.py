#!/usr/bin/env python3
"""
Database Clearing Script for User Notes API
Run this script to clear all data from the database tables.
WARNING: This will permanently delete all users and notes!
"""

from database import db
from models import User, Note
from config import Config
from flask import Flask
import sys

def clear_database():
    """Clear all data from database tables"""
    app = Flask(__name__)
    app.config.from_object(Config)

    try:
        db.init_app(app)
        with app.app_context():
            print("🗑️  Database Clearing Operation")
            print("=" * 50)
            print("WARNING: This will delete ALL users and notes permanently!")
            print()

            # Show current data before clearing
            users_count = User.query.count()
            notes_count = Note.query.count()

            print(f"Current data: {users_count} users, {notes_count} notes")
            print()

            # Ask for confirmation
            if len(sys.argv) > 1 and sys.argv[1] == "--yes":
                confirm = "yes"
            else:
                confirm = input("Are you sure you want to clear all data? Type 'yes' to confirm: ").strip().lower()

            if confirm != "yes":
                print("❌ Operation cancelled.")
                return

            # Clear the tables (delete in correct order due to foreign keys)
            print("🧹 Clearing database...")

            # Delete all notes first (due to foreign key constraint)
            notes_deleted = Note.query.delete()
            print(f"   Deleted {notes_deleted} notes")

            # Then delete all users
            users_deleted = User.query.delete()
            print(f"   Deleted {users_deleted} users")

            # Commit the changes
            db.session.commit()

            print("✅ Database cleared successfully!")
            print("   All users and notes have been permanently deleted.")

    except Exception as e:
        print(f"❌ Error clearing database: {str(e)}")
        print("Make sure the database is running and accessible.")

def reset_database():
    """Drop and recreate all tables (more thorough reset)"""
    app = Flask(__name__)
    app.config.from_object(Config)

    try:
        db.init_app(app)
        with app.app_context():
            print("🔄 Database Reset Operation")
            print("=" * 50)
            print("WARNING: This will DROP and RECREATE all tables!")
            print("All data will be permanently lost!")
            print()

            # Ask for confirmation
            if len(sys.argv) > 1 and sys.argv[1] == "--yes":
                confirm = "yes"
            else:
                confirm = input("Are you sure you want to reset the database? Type 'yes' to confirm: ").strip().lower()

            if confirm != "yes":
                print("❌ Operation cancelled.")
                return

            print("🔨 Dropping tables...")
            db.drop_all()

            print("🏗️  Recreating tables...")
            db.create_all()

            print("✅ Database reset successfully!")
            print("   All tables have been recreated (empty).")

    except Exception as e:
        print(f"❌ Error resetting database: {str(e)}")
        print("Make sure the database is running and accessible.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        clear_database()