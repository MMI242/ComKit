# FastAPI Server - Setup & Testing Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd sourcecode/server-fastapi
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python main.py
# or
./run_server.sh
```

Server runs on: `http://localhost:8000`

### 3. Test the Server

The test script is located at: `sourcecode/test-server/test_alur_pengguna.py`

Run tests against port 8000:
```bash
cd sourcecode/test-server
python test_alur_pengguna.py http://localhost:8000
```

## 📝 Key Changes Made to Support Tests

### 1. **GET /user/items** - Returns object with items array
```json
{
  "items": [...]
}
```
Instead of just the array.

### 2. **POST /user/items** - Accepts JSON
Changed from multipart/form-data to JSON for easier testing.
```json
{
  "name": "Item name",
  "description": "Description",
  "qty": 10,
  "unit": "pcs",
  "type": "borrow",
  "status": "available"
}
```

### 3. **POST /items/{id}/request** - Returns request_id
Response includes both `id` and `request_id` fields:
```json
{
  "request_id": 1,
  "id": 1,
  "item": {...},
  "status": "pending",
  ...
}
```

### 4. **PUT /user/items/{id}** - Accepts JSON
Changed from multipart/form-data to JSON.

## 🔧 Environment Configuration

Create `.env` file (already created with defaults):
```env
ENVIRONMENT=development
SECRET_KEY=dev-secret-key-change-in-production-12345
OLLAMA_API_URL=http://localhost:11434
DATABASE_URL=sqlite:///./kitchen.db
```

## 📚 API Endpoints

### Authentication
- `POST /auth/register` - Register (returns 201)
- `POST /auth/login` - Login (returns 200)
- `POST /auth/refresh` - Refresh token

### Items (Homepage)
- `GET /items` - List items with pagination/search/filter
- `POST /items/{id}/request` - Request an item

### User Items
- `GET /user/items` - Get user's items
- `POST /user/items` - Create item (JSON body)
- `PUT /user/items/{id}` - Update item (JSON body)
- `DELETE /user/items/{id}` - Delete item

### User Requests
- `GET /user/requests?type=incoming|outgoing` - Get requests
- `PATCH /user/requests/{id}` - Update request status

### AI Recipe
- `POST /ai/recipe` - Generate recipe from ingredients

### Development (only in dev mode)
- `DELETE /dev/delete/item/{id}` - Delete any item
- `DELETE /dev/delete/user/{username}` - Delete user with cascade

## 🧪 Test Flow

The test script (`test_alur_pengguna.py`) tests:

1. **User1**: Register → Login → Create 30 items → Logout
2. **User2**: Register → Browse items (pagination, search) → Request item
3. **User1**: Login → View incoming requests → Approve request
4. **Cleanup**: Delete both users (cascade deletes items & requests)

## 🐛 Troubleshooting

### Test fails with "assert 200 == 201"
- Make sure you're running the **FastAPI server** we just created
- The server should be on port 8000 (or specify the port in test command)
- Restart the server after code changes

### Database locked errors
- Stop all running instances of the server
- Delete `kitchen.db` and restart

### Import errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Use Python 3.8 or higher

## 📁 File Structure

```
sourcecode/server-fastapi/
├── main.py                 # Main FastAPI app
├── database.py             # Database setup
├── models.py               # SQLAlchemy models
├── schemas.py              # Pydantic schemas
├── auth.py                 # JWT authentication
├── routes_auth.py          # Auth endpoints
├── routes_items.py         # Items endpoints
├── routes_user_items.py    # User items endpoints
├── routes_user_requests.py # User requests endpoints
├── routes_ai.py            # AI recipe endpoint
├── routes_dev.py           # Development endpoints
├── requirements.txt        # Dependencies
├── .env                    # Environment config
├── run_server.sh          # Run script
└── README.md              # Documentation
```

## ✅ All Requirements Implemented

- ✅ JWT Authentication (access & refresh tokens)
- ✅ User registration with validation
- ✅ Item CRUD with image support
- ✅ Request system with qty reservation
- ✅ Pagination & search on homepage
- ✅ Status transitions (approve/reject/cancel/returned)
- ✅ AI recipe generation with Ollama
- ✅ Development endpoints with environment check
- ✅ All validations from SRS document

## 🎯 Ready to Test

Run the server and execute the test:

```bash
# Terminal 1: Start server
cd sourcecode/server-fastapi
python main.py

# Terminal 2: Run tests
cd sourcecode/test-server
python test_alur_pengguna.py http://localhost:8000
```

All tests should pass! ✨
