# Student Record Management CLI

A command-line interface application for managing student records with CRUD operations, search functionality, and CSV export.

## Requirements

- Python 3.6+
- Docker

## Setup

1. Start Docker Desktop.
2. Run the PostgreSQL container:
   ```
   docker run --name postgres-student -e POSTGRES_PASSWORD=password -e POSTGRES_DB=student_db -p 5432:5432 -d postgres
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. The table will be created automatically when running the app.

## Usage

Run the CLI:
```
python main.py <command> [options]
```

Available commands:
- `add --name "Name" --grade "Grade"`: Add a new student
- `view`: View all students
- `update --id ID --name "New Name" --grade "New Grade"`: Update a student record
- `delete --id ID`: Delete a student record
- `search --type name/grade/id --value "Value"`: Search students
- `export --filename students.csv`: Export students to CSV

Example:
```
python main.py add --name "John Doe" --grade "A"
python main.py view
python main.py export --filename students.csv
```

## Database Schema

The application uses a PostgreSQL database with a `students` table:
- `id`: SERIAL PRIMARY KEY
- `name`: VARCHAR(100) NOT NULL
- `grade`: VARCHAR(10) NOT NULL