# Bookmark URL Shortener API

A modern, secure, and extensible URL shortener service built with FastAPI, SQLAlchemy (async), Alembic, and PostgreSQL.

## Why This Project?

- **Problem:** Long URLs are hard to share, remember, and manage. There is a need for a simple, secure, and user-friendly way to shorten URLs, track usage, and manage bookmarks.
- **Solution:** This project provides a robust API for user registration, authentication, bookmark (URL) creation, redirection, and analytics, with a focus on clean code, security, and extensibility.

## Features
- User registration and JWT-based authentication
- Create short URLs (bookmarks) for any valid URL
- Redirect to the original URL using the short code
- Track visit counts for each bookmark
- Get all bookmarks for a user
- Get, delete bookmarks by ID
- Async database operations for high performance
- CORS support and enhanced logging

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy (async), Alembic
- **Database:** PostgreSQL
- **Auth:** JWT (JSON Web Tokens)
- **Other:** Pydantic, passlib (bcrypt), requests (for testing)

## Project Structure
```
src/
  routes/
    auth.py         # Auth endpoints (register, login)
    bookmarks.py    # Bookmark CRUD endpoints
    redirects.py    # Redirection endpoint
  models/           # SQLAlchemy models
  schemas/          # Pydantic schemas
  utils/            # Auth, shortener, helpers
  main.py           # FastAPI app entrypoint
alembic/             # DB migrations
requirements.txt     # Python dependencies
```

## API Workflow

1. **Register a User**
   - `POST /auth/register`
   - Body: `{ "username": ..., "email": ..., "password": ... }`
   - Registers a new user. Returns user info.

2. **Login**
   - `POST /auth/login`
   - Body: `username`, `password` (form data)
   - Returns JWT access token.

3. **Create a Bookmark (Shorten URL)**
   - `POST /bookmarks/create`
   - Headers: `Authorization: Bearer <token>`
   - Body: `{ "original_url": "https://..." }`
   - Returns bookmark info with short code.

4. **Redirect**
   - `GET /<short_code>`
   - Redirects to the original URL and increments visit count.

5. **Get All Bookmarks**
   - `GET /bookmarks/get/all`
   - Headers: `Authorization: Bearer <token>`
   - Returns all bookmarks for the user.

6. **Get Bookmark by ID**
   - `GET /bookmarks/get/{bookmark_id}`
   - Headers: `Authorization: Bearer <token>`
   - Returns bookmark details.

7. **Delete Bookmark**
   - `DELETE /bookmarks/delete/{bookmark_id}`
   - Headers: `Authorization: Bearer <token>`
   - Deletes the bookmark if owned by the user.

## How to Run

1. **Clone the repo and install dependencies:**
   ```sh
   git clone <repo-url>
   cd FASTAPI_SQL
   python -m venv venv
   venv\Scripts\activate  # On Windows
   pip install -r requirements.txt
   ```
2. **Configure your database in `src/config.py`**
3. **Run Alembic migrations:**
   ```sh
   alembic upgrade head
   ```
4. **Start the server:**
   ```sh
   uvicorn src.main:app --reload
   ```
5. **Visit the docs:**
   - Open [http://localhost:8000/docs](http://localhost:8000/docs)

## Example Workflow (with Python requests)
See `test_login.py` for a full example of registration, login, bookmark creation, and retrieval.

## RTC (Ready To Contribute)
- The project is modular and ready for contributions.
- You can add features like custom domains, analytics, admin panel, etc.
- Please open issues or pull requests for suggestions and improvements.


