# Week 7: Routing and Serializers

## Topics
- URL routing
- Request/response handling
- Serializers

## Assignment
Add public sharing of notes via unique URL with optional expiration date.

## Requirements
- Generate unique sharable links.
- Add link expiration date option.
- Track link access count.
- Deliverables: API endpoints + Postman tests.

## Implementation Status
- Step 1 (Week Setup): Completed
- Step 2 (Routing Design): Completed
- Step 3 (Data Model Changes): Completed
- Step 4 (Unique Share Link Generation): Completed
- Step 5 (Serializer Layer): Completed
- Step 6 (Request/Response Handling): Completed
- Step 7 (Share Endpoints): Completed
- Step 8 (Access Count Tracking): Completed
- Step 9 (CRUD/Service Logic): Completed
- Step 10 (Postman Deliverables): Completed
- Step 11 (File Responsibilities): Completed

## Current Endpoints (Week 7)
- `POST /notes/<note_id>/share`
- `GET /notes/<note_id>/shares`
- `PATCH /notes/<note_id>/shares/<share_id>`
- `DELETE /notes/<note_id>/shares/<share_id>`
- `GET /s/<token>`

## Run and Test
1. Set database URL (PowerShell):
  - `$env:DATABASE_URL = "postgresql+pg8000://user:password@localhost:5432/notes_db"`
2. Start API:
  - `python main.py`
3. Run automated tests:
  - `python test_api.py`
4. Run Postman collection:
  - `notes_api.postman_collection.json`

## Implementation Strategy

### 1. Week Setup
- Use `week-6` as the baseline and implement all week-7 work inside `week-7/`.
- Keep existing auth and note CRUD behavior stable.
- Add only sharing features and routing/serialization improvements needed for week-7.

### 2. Routing Design
- Refactor `main.py` to register route groups by feature.
- Suggested route groups:
  - Auth routes: registration/login/logout.
  - Note routes: existing owner note CRUD.
  - Share routes (owner-only): create/list/update/revoke links for owned notes.
  - Public routes: access shared notes by token without JWT.
- Keep endpoint naming simple and consistent.

### 3. Data Model Changes
- Add a `ShareLink` model tied to `Note`.
- Recommended fields:
  - `id`
  - `note_id` (FK)
  - `token` (unique, indexed)
  - `expires_at` (nullable datetime)
  - `access_count` (default 0)
  - `created_at`
  - `last_accessed_at` (nullable)
  - `is_revoked` (default False)
- Add indexes for `token` and `note_id` for faster lookup.

### 4. Unique Share Link Generation
- Generate token with Python `secrets` module (for example `token_urlsafe`).
- On create share link:
  - Generate token.
  - Ensure token uniqueness (retry on collision).
  - Build public URL using app base path and token.

### 5. Serializer Layer
- Add `serializers.py` for clear request/response transformation.
- Suggested serializer helpers:
  - `serialize_note(note)`
  - `serialize_share_link(share_link, base_url)`
  - `serialize_public_note(note, share_link)`
  - `parse_share_payload(data)`
- Keep route functions thin: validate input, call CRUD/service, return serialized response.

### 6. Request and Response Handling
- Standardize API response shape and status codes.
- Validate inputs:
  - `expires_at` is optional.
  - If provided, must be valid ISO datetime and in the future.
- Suggested errors:
  - `400` for invalid request data.
  - `401` for auth failures.
  - `403` for unauthorized note ownership.
  - `404` for missing note/share token.
  - `410` for expired/revoked share links.

### 7. Share Endpoint Plan
- Owner endpoints (JWT required):
  - `POST /notes/<note_id>/share` create share link.
  - `GET /notes/<note_id>/shares` list links for note.
  - `PATCH /notes/<note_id>/shares/<share_id>` update expiration or revoke.
  - `DELETE /notes/<note_id>/shares/<share_id>` remove/revoke link.
- Public endpoint (no JWT):
  - `GET /s/<token>` return shared note when link is active.

### 8. Access Count Tracking
- Increment `access_count` only on successful public access.
- Update `last_accessed_at` during successful access.
- Do not increment for invalid, expired, or revoked token requests.

### 9. CRUD and Service Logic
- In `crud.py` (or a new share service module), add methods to:
  - Create share links.
  - Resolve share token to note.
  - Validate expiration and revoke state.
  - Increment access count atomically.
  - List and manage links by note owner.

### 10. Postman Deliverables
- Update `notes_api.postman_collection.json` with a Week 7 folder.
- Add test flows:
  - Create link without expiration.
  - Create link with expiration.
  - Access public link and assert note payload.
  - Access link multiple times and assert `access_count` increments.
  - Access expired/revoked link and assert failure status.
  - Non-owner attempts link management and gets forbidden/not found.

### 11. Suggested File Responsibilities
- `models.py`: `ShareLink` model and relationships.
- `crud.py`: share-link data operations, token resolution, and access counting.
- `serializers.py`: all payload serializers/parsers and response helpers.
- `main.py`: app setup and blueprint registration.
- `routes/auth_routes.py`: auth endpoints.
- `routes/note_routes.py`: note/category/tag endpoints.
- `routes/share_routes.py`: owner-only share management endpoints.
- `routes/public_routes.py`: public token endpoint (`GET /s/<token>`).
- `test_api.py`: automated Week 7 API tests (including counter and expiry/revoke checks).
- `notes_api.postman_collection.json`: Postman test flows for Week 7 sharing requirements.

## Definition of Done
- All sharing endpoints implemented and reachable.
- Public token URL works with optional expiration.
- Access count is persisted and correct.
- Postman collection demonstrates success and failure scenarios.
- README reflects the final API contract.