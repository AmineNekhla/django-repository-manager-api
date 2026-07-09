# Django Repository Manager API

A production-ready REST API built with Django and Django REST Framework for managing code repositories and their files. This project was developed as a technical challenge and follows professional backend practices such as Clean Architecture, Custom QuerySets, DRF Validation, and robust filtering.

## 🚀 Features
- **Repository Management:** Create, list, and retrieve repositories.
- **CodeFile Management:** Add and manage code files linked to repositories.
- **Advanced Searching:** Search files by name, language, or file type.
- **Robust Filtering & Ordering:** Filter files by size ranges, exact language, or exact type. Order results automatically.
- **Critical File Detection:** A specialized `/api/files/critical/` endpoint to instantly flag configuration files, security files, massive files, or undocumented files using highly optimized database queries.
- **Business Logic Layer:** Service-oriented architecture and Custom DRF Exceptions ensuring solid data integrity.
- **Comprehensive Testing:** 13 Automated test cases covering CRUD, search, detection, and validation logic.

---

## 💻 Installation and Setup

### 1. Clone the repository and navigate to the project directory:
*(Ensure you are inside the `django_assignment` folder)*

### 2. Create and activate a Virtual Environment
**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```
**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Start the Server
```bash
python manage.py runserver
```

---

## 🧪 Running Tests
This project includes comprehensive tests covering validation, critical logic, CRUD operations, and search endpoints.
```bash
python manage.py test
```
All 13 tests should pass seamlessly.

---

## 📡 API Endpoints & Examples

### Repositories
- `GET /api/repositories/` - List all repositories
- `POST /api/repositories/` - Create a new repository
- `GET /api/repositories/{id}/` - Retrieve a specific repository
- `PUT /api/repositories/{id}/` - Update a repository
- `DELETE /api/repositories/{id}/` - Delete a repository

**Example POST Request (Create Repository):**
```json
POST /api/repositories/
{
    "name": "My Backend Project",
    "owner": "Amine",
    "description": "A REST API challenge."
}
```

### Files
- `GET /api/files/` - List all files (Paginated)
- `POST /api/files/` - Create a file
- `GET /api/files/{id}/` - Retrieve a file

**Example POST Request (Create File):**
```json
POST /api/files/
{
    "repository": 1,
    "name": "script.py",
    "path": "/src",
    "file_type": "python",
    "language": "python",
    "size": 1024,
    "description": "Main logic"
}
```

### Search & Filtering Examples
You can combine these parameters!
- **Search by keyword:** `/api/files/?search=config`
- **Filter by Language:** `/api/files/?language=Python`
- **Filter by Size Range:** `/api/files/?min_size=1000&max_size=50000`
- **Ordering (Largest First):** `/api/files/?ordering=-size`

### Critical Files
- `GET /api/files/critical/` 
Returns only files that match our strict critical business rules (e.g. `.env`, `settings.py`, missing descriptions, or file size > 1MB).
