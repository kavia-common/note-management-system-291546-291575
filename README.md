# note-management-system-291546-291575

## Notes Backend API

Base URL:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/swagger.json`
- API base: `/api/`

### Health
- GET `/api/health/` → 200: `{"message": "Server is up!"}`

### Notes
- List + Create: `/api/notes/`
  - GET: List notes with pagination.
    - Query params:
      - `page` (int), `page_size` (int, default 10, max 100)
      - `search` (str) - fuzzy search by title
      - `title` (str) - filter contains by title
  - POST: Create a note
    - Body: `{ "title": "string", "content": "string" }`
    - 201 Created → JSON note

- Detail: `/api/notes/{id}/`
  - GET: Retrieve note by id
  - PUT: Update entire note
  - PATCH: Partial update
  - DELETE: Delete note

Fields:
- `id` (int, read-only)
- `title` (string, required, max 255)
- `content` (string, optional)
- `created_at` (datetime, read-only)
- `updated_at` (datetime, read-only)

### Status Codes
- 200 OK, 201 Created, 204 No Content, 400 Bad Request, 404 Not Found

### Run locally
This container runs on port 3001. With Django settings configured for SQLite, migrations are included.

To create and apply migrations (already provided):
- `python manage.py migrate`

```bash
# Smoke test (optional)
python manage.py test
```
