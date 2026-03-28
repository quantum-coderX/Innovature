# Week 6: ORM & Relationships

## Topics
- Models, migrations
- One-to-many and many-to-many relationships
- Querysets and filters

## Assignment
Extend Notes API with categories/tags, filter by category/tag, and search notes by keyword.

## Requirements
- Add categories (one-to-many).
- Add tags (many-to-many).
- Implement filter by category/tag.
- Add keyword search.
- Deliverables: Updated API + Postman test cases.

## Implementation Strategy

### 1. Project Setup
- Copy the structure from week-5 as the base.
- Ensure all dependencies are installed (Flask, SQLAlchemy, Flask-Migrate, etc.).
- Set up the database and migrations.

### 2. Database Models
- **Category Model**: Represents categories for notes (one-to-many with notes).
  - Fields: id, name, created_at, updated_at.
  - Relationship: One category can have many notes.

- **Tag Model**: Represents tags for notes (many-to-many with notes).
  - Fields: id, name, created_at, updated_at.
  - Relationship: Many tags can be associated with many notes (use association table).

- **Note Model Update**:
  - Add foreign key to Category.
  - Add many-to-many relationship with Tag.

### 3. Migrations
- Use Flask-Migrate to create and apply migrations for new models and relationships.
- Run `flask db migrate` and `flask db upgrade`.

### 4. API Endpoints
- **Categories**:
  - GET /categories: List all categories.
  - POST /categories: Create a new category.
  - GET /categories/<id>: Get a specific category.
  - PUT /categories/<id>: Update a category.
  - DELETE /categories/<id>: Delete a category.

- **Tags**:
  - GET /tags: List all tags.
  - POST /tags: Create a new tag.
  - GET /tags/<id>: Get a specific tag.
  - PUT /tags/<id>: Update a tag.
  - DELETE /tags/<id>: Delete a tag.

- **Notes Updates**:
  - Update POST /notes to accept category_id and tags (list of tag ids).
  - Update PATCH /notes/<id> similarly.
  - Add GET /notes?category=<id> to filter notes by category.
  - Add GET /notes?tag=<id> to filter notes by tag.
  - Add GET /notes?search=<keyword> to search notes by keyword in title or content.

### 5. Querysets and Filters
- Use SQLAlchemy querysets to filter notes by category, tag, or keyword.
- For keyword search, use `like` or `ilike` for case-insensitive search.

### 6. Testing with Postman
- Update the Postman collection from week-5.
- Add test cases for:
  - Creating categories and tags.
  - Creating notes with categories and tags.
  - Filtering notes by category and tag.
  - Searching notes by keyword.
  - Ensure all CRUD operations work with the new relationships.

### 7. Validation and Error Handling
- Validate that category exists when creating/updating notes.
- Handle cases where tags don't exist.
- Return appropriate error messages.

### 8. Code Structure
- models.py: Define Category, Tag, and updated Note models.
- crud.py: Update functions to handle relationships.
- main.py: Add new routes and update existing ones.
- test_api.py: Add tests for new functionality.

### Next Steps
- Start by defining the models.
- Create migrations.
- Implement the API endpoints.
- Test thoroughly with Postman.