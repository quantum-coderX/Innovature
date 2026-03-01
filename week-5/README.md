# Week 5: User Notes API

This is a fully implemented User Notes API built with Flask, featuring JWT authentication, CRUD operations for personal notes, PostgreSQL database, comprehensive error handling, and logging.

## Features
- **JWT Authentication**: Secure login/logout with token-based auth.
- **CRUD Operations**: Create, read, update, delete personal notes (user-specific).
- **Password Security**: Strong validation (8+ chars, uppercase, lowercase, digit).
- **Database**: PostgreSQL via Docker for data persistence.
- **Error Handling**: Comprehensive try-except blocks with proper HTTP status codes.
- **Logging**: Detailed logs to console and file (`api.log`) for monitoring.
- **JSON REST API**: All responses are JSON-compliant.

## Requirements Met
- ✅ JWT login/logout
- ✅ CRUD operations for personal notes (user-specific)
- ✅ JSON REST-compliant responses
- ✅ Postman collection for testing
- ✅ Working API (local with Docker)

## Setup
1. **Environment setup**: Copy `.env` and update secrets:
   ```bash
   cp .env .env.local  # Edit with your actual values
   ```
2. **Start PostgreSQL**: `docker-compose up -d`
3. **Install Dependencies**: `pip install -r requirements.txt`
4. **Run the API**: `python main.py`
5. **Test**: Use Postman collection or curl commands.

To stop the database: `docker-compose down`

## Environment Variables
The app uses environment variables for configuration. Copy `.env` to `.env.local` and update:

- `SECRET_KEY`: Random string for Flask security
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Random string for JWT tokens

Example:
```
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=postgresql+pg8000://user:pass@localhost:5432/notes_db
JWT_SECRET_KEY=your-jwt-secret-key-here
```

## API Endpoints
### Authentication
- `POST /auth/register` - Register new user (with password validation)
- `POST /auth/login` - Login and get JWT token
- `POST /auth/logout` - Logout (client-side token discard)

### Notes (JWT Required)
- `GET /notes` - List all user's notes
- `POST /notes` - Create a new note
- `GET /notes/{note_id}` - Get a specific note
- `PUT /notes/{note_id}` - Update a note
- `DELETE /notes/{note_id}` - Delete a note

### Health Check
- `GET /` - API status check

## Testing with Postman
1. Import `notes_api.postman_collection.json`.
2. Set `base_url` variable to `http://localhost:5000`.
3. Run requests in order: Register → Login → CRUD operations.

## Logs
- **Console**: Real-time logs in terminal.
- **File**: `api.log` for persistent logs.
- Tracks user actions, errors, and API usage.

## Technologies
- Flask (web framework)
- Flask-JWT-Extended (JWT auth)
- Flask-SQLAlchemy (ORM)
- PostgreSQL (database)
- pg8000 (DB driver)
- Werkzeug (password hashing)
- python-dotenv (environment management)
- Docker (database container)

## Security
- Passwords hashed with PBKDF2.
- JWT tokens for session management.
- User-specific data isolation.
- Input validation and error handling.

## Deliverables
- Postman collection: `notes_api.postman_collection.json`
- Working API (local)