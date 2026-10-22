# django-repository-manager-api

A REST API built with Django and Django REST Framework for managing code repositories and their files. I built this as a technical challenge.

## What it does

- Create and list repositories
- Add code files linked to a repository
- Search files by name, language, or type
- Filter by size range, exact language, order results
- A /api/files/critical/ endpoint that flags config files, security files, large files, or undocumented ones
- 13 automated tests covering the main flows

## Setup

`ash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
`

Make sure you're inside the django_assignment folder before running these.

## Tests

`ash
python manage.py test
`

All 13 tests should pass.

## API overview

**Repositories**
- GET /api/repositories/ — list all
- POST /api/repositories/ — create one
- GET/PUT/DELETE /api/repositories/{id}/ — get, update, delete

**Files**
- GET /api/files/ — list (paginated)
- POST /api/files/ — create
- GET /api/files/{id}/ — get one
- GET /api/files/critical/ — get flagged files

**Search and filters:**
- /api/files/?search=config — keyword search
- /api/files/?language=Python — filter by language
- /api/files/?min_size=1000&max_size=50000 — size range
- /api/files/?ordering=-size — sort by size descending