# Week 5: User Notes API

This is a skeleton for a User Notes API built with Flask, featuring JWT authentication and CRUD operations for personal notes.

## Requirements
- JWT login/logout
- CRUD operations for personal notes (user-specific)
- JSON REST-compliant responses

## Setup
1. Start PostgreSQL with Docker: `docker-compose up -d`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `python main.py`

To stop the database: `docker-compose down`

## API Endpoints
- POST /auth/register
- POST /auth/login
- POST /auth/logout
- GET /notes
- POST /notes
- GET /notes/{note_id}
- PUT /notes/{note_id}
- DELETE /notes/{note_id}

## Deliverables
- Postman collection: `notes_api.postman_collection.json`
- Working API (local)