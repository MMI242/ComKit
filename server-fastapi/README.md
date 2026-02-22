# Kitchen Sharing FastAPI Server

Simple FastAPI server for community kitchen item sharing application.

## Setup

1. Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python main.py
```

Server will run on `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Requirements

- Python 3.8+
- Ollama (for AI recipe generation)




## Project Structure

    sourcecode/server-fastapi/
    ├── main.py                      # Main FastAPI application
    ├── database.py                  # Database configuration
    ├── models.py                    # SQLAlchemy models (User, Item, Request)
    ├── schemas.py                   # Pydantic schemas for validation
    ├── auth.py                      # JWT authentication utilities
    ├── routes_auth.py              # Auth endpoints (login, register, refresh)
    ├── routes_items.py             # Items endpoints (list, request)
    ├── routes_user_items.py        # User items CRUD endpoints
    ├── routes_user_requests.py     # User requests endpoints
    ├── routes_ai.py                # AI recipe generation
    ├── routes_dev.py               # Development-only endpoints
    ├── requirements.txt            # Python dependencies
    ├── .env                        # Environment configuration
    ├── .env.example                # Example environment file
    ├── .gitignore                  # Git ignore rules
    └── README.md                   # Documentation


## Features Implemented

Features Implemented
### Authentication (/auth)
    POST /auth/login - Login with username & password
    POST /auth/register - Register new user (auto-login)
    POST /auth/refresh - Refresh access token
### Items (/items)
    GET /items - List all items (with pagination, search, filter)
    POST /items/{id}/request - Request an item
### User Items (/user/items)
    GET /user/items - Get all user's items
    POST /user/items - Create new item (with photo upload)
    PUT /user/items/{id} - Update item
    DELETE /user/items/{id} - Delete item
### User Requests (/user/requests)
    GET /user/requests?type=incoming - Get incoming requests
    GET /user/requests?type=outgoing - Get outgoing requests
    PATCH /user/requests/{id} - Update request status (approve/reject/cancel/returned)
### AI Recipe (/ai)
    POST /ai/recipe - Generate recipe from ingredients using Ollama
### Development Endpoints (dev)
    DELETE /dev/delete/item/{id} - Delete any item (dev only)
    DELETE /dev/delete/user/{username} - Delete user with cascade (dev only)
