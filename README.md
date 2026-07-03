# Birthday Universe – Rahul ❤️ Raksitha

A Flask + MySQL (SQLAlchemy ORM) web app that lets visitors submit birthday wishes (optional photo uploads) and view them on the wishes wall.

---

## Project Overview

- **Frontend:** Vanilla HTML/CSS/JavaScript (already completed)
- **Backend:** Python **Flask**, **Flask-SQLAlchemy** ORM, **Flask-Migrate** (Alembic)
- **Database:** **MySQL 8+**
- **Uploads:** Photos saved under the server-side `uploads/` directory and served via `/uploads/<filename>`.

---

## Features

- Submit wishes with required visitor name + wish message
- Optional photo upload (jpg/jpeg/png/webp, max 5MB)
- Photos are served securely from `/uploads/<filename>`
- Wishes are displayed in newest-first order
- Database migrations supported via Flask-Migrate

---

## Architecture (High Level)

- `app/__init__.py`
  - Flask app factory
  - Initializes SQLAlchemy and Flask-Migrate
  - Registers API blueprints
  - Serves static frontend files
- `app/extensions.py`
  - Holds `db = SQLAlchemy()` and `migrate = Migrate()`
- `app/models/*`
  - SQLAlchemy ORM models only
- `app/routes/*`
  - API endpoints (wishes + uploads)
- `migrations/*`
  - Alembic environment for Flask-Migrate

---

## Folder Structure

```text
. \
├── app/ \
│   ├── __init__.py \
│   ├── config.py \
│   ├── config_factory.py \
│   ├── extensions.py \
│   ├── logging_config.py \
│   ├── models/ \
│   │   ├── __init__.py \
│   │   ├── wishes.py \
│   │   └── uploads.py \
│   └── routes/ \
│       ├── health.py \
│       └── wishes.py \
├── migrations/ \
│   ├── alembic.ini \
│   └── versions/ \
├── js/ \
├── css/ \
├── assets/ \
├── uploads/ \
├── run.py \
├── requirements.txt \
└── README.md
```

---

## Tech Stack

### Frontend
- HTML5
- CSS3
- Vanilla JavaScript

### Backend
- Flask
- Flask SQLAlchemy
- Flask Migrate
- PyMySQL

### Database
- MySQL 8+

---

## Installation Guide

### 1) Create and activate a virtual environment

```bash
python -m venv .venv
# Windows (PowerShell)
.venv\\Scripts\\Activate.ps1
```

### 2) Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file (example provided in repository).

Required variables for production-like operation:
- `SECRET_KEY`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_DATABASE` (defaults to `birthday_universe`)

Optional:
- `UPLOAD_FOLDER` (defaults to `uploads`)
- `MAX_CONTENT_LENGTH` (defaults to 5MB)
- `FLASK_ENV` (`development|testing|production`)
- `FLASK_DEBUG`

---

## MySQL Setup

1. Install and start **MySQL 8+**
2. Create the database:

- **Database name:** `birthday_universe`
- **Character set / collation:** `utf8mb4` / `utf8mb4_unicode_ci`

---

## Database Migrations (Flask-Migrate)

This project uses **Flask-Migrate** (Alembic).

> Run commands from the project root.

### Initialize migrations (only if migrations are missing)

```bash
flask db init
```

### Generate a new migration

```bash
flask db migrate -m "Describe schema change"
```

### Apply migrations

```bash
flask db upgrade
```

### Rollback

```bash
flask db downgrade
```

---

## Run Instructions

### Start the server

```bash
python run.py
```

By default (in `run.py`):
- `http://127.0.0.1:5000`

---

## API Endpoints

### 1) Health

- **Purpose:** Basic service health check
- **Method:** `GET`
- **URL:** `/api/health`
- **Request:** none
- **Response:** JSON health payload
- **Status Codes:** `200`

### 2) Get Wishes

- **Purpose:** Retrieve active wishes (newest first)
- **Method:** `GET`
- **URL:** `/api/wishes`
- **Request:** none
- **Response JSON Example:**

```json
{
  "success": true,
  "message": "Wishes retrieved successfully",
  "data": {
    "wishes": [
      {
        "id": 1,
        "name": "Visitor",
        "message": "Wish message",
        "photo_url": "/uploads/<stored_name>",
        "createdAt": "<day> <Month> <year>"
      }
    ]
  }
}
```

- **Status Codes:**
  - `200` success
  - `500` if DB unavailable

### 3) Create Wish

- **Purpose:** Create a wish (and optional photo upload)
- **Method:** `POST`
- **URL:** `/api/wishes`
- **Request:** `multipart/form-data`
  - `visitor_name` (required)
  - `wish_message` (required)
  - `photo` (optional)

- **Validation Rules (backend enforced):**
  - `visitor_name` required, 2–100 chars
  - `wish_message` required, max 300 chars
  - `photo` if present:
    - extension must be one of `jpg`, `jpeg`, `png`, `webp`
    - MIME type must be one of `image/png`, `image/jpeg`, `image/jpg`, `image/webp`
    - max size 5MB

- **Response JSON Example (success):**

```json
{
  "success": true,
  "message": "Wish created successfully",
  "data": {
    "id": 1,
    "name": "Visitor",
    "message": "Wish message",
    "photo_url": "/uploads/<stored_name>",
    "createdAt": "<day> <Month> <year>"
  }
}
```

- **Status Codes:**
  - `201` success
  - `400` validation failed
  - `500` DB error

### 4) Serve Upload

- **Purpose:** Serve uploaded photos securely
- **Method:** `GET`
- **URL:** `/uploads/<filename>`
- **Request:** none
- **Response:** raw image file
- **Status Codes:**
  - `200` if exists
  - `404` JSON if missing

---

## Database Documentation

### Database Name
- `birthday_universe`

### Tables

#### `wishes`
- `id` (PK, autoincrement)
- `visitor_name` (NOT NULL, varchar)
- `wish_message` (NOT NULL, varchar)
- `photo_filename` (nullable)
- `photo_url` (nullable)
- `created_at` (NOT NULL, default `utcnow`, indexed)
- `status` (NOT NULL, default `'active'`, indexed)

Indexes:
- `created_at` (via model)
- `status` (via model)

#### `uploads`
- `id` (PK, autoincrement)
- `original_name` (NOT NULL)
- `stored_name` (NOT NULL, **UNIQUE**)
- `mime_type` (NOT NULL)
- `file_size` (NOT NULL)
- `uploaded_at` (NOT NULL, default `utcnow`)

---

## Deployment Instructions

This backend is compatible with typical WSGI deployment.

### Environment variables
Ensure `.env` (or system env vars) is configured with MySQL + SECRET_KEY.

### Gunicorn (example)

```bash
gunicorn "run:app" -w 2 -b 0.0.0.0:8000
```

---

## Troubleshooting

### Common Errors

- **DB connection fails**
  - Verify `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`
  - Confirm MySQL is running and accessible from the host running Flask.

- **Uploads not found (404)**
  - Ensure upload directory exists: `uploads/`
  - Confirm files are saved and permissions allow reading.

- **Migration conflicts**
  - Confirm migrations are incremental (do not recreate history)

---

## FAQ

- **Why `utf8mb4_unicode_ci`?**
  - Ensures robust UTF-8 compatibility for names/messages.

---

## Future Improvements

- Add server-side image content verification (magic-number sniffing) for stronger MIME integrity.
- Add rate limiting and CSRF strategy for form submissions.
- Improve health endpoint details.

---

## Known Limitations

- MIME validation relies on `photo_file.content_type` (client-provided header). Extension and content-type are both checked, but deeper content sniffing is not performed.

---

## Author

Rahul ❤️ Raksitha

---

## License

(Use your project license here)

"# Surprise" 
