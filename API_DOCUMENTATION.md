# ComKit Kitchen Sharing API Documentation

## Overview

ComKit is a community kitchen sharing platform that allows users to share and borrow kitchen items. This API provides endpoints for authentication, item management, request handling, and AI-powered recipe generation.

## Base URL

```
http://localhost:8000
```

## Authentication

The API uses JWT tokens for authentication. Tokens can be passed via:
- HTTP-only cookies (set automatically on login/register)
- Authorization header: `Bearer <token>`

## API Endpoints

### Authentication

#### POST /auth/login
Authenticate user and receive access tokens.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "access_token": "string",
    "refresh_token": "string",
    "token_type": "Bearer",
    "expires_in": 3600,
    "user": {
        "id": 1,
        "username": "string",
        "name": "string",
        "address": "string"
    }
}
```

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
    "username": "string (min 3 chars, lowercase, alphanumeric + underscore)",
    "password": "string (min 6 chars)",
    "name": "string",
    "address": "string"
}
```

#### POST /auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
    "refresh_token": "string"
}
```

#### GET /auth/validate-cookies
Validate authentication cookies and return user info.

#### POST /auth/clear-cookies
Clear authentication cookies (logout).

### Items

#### GET /items
Get paginated list of all available items.

**Query Parameters:**
- `page`: Page number (default: 1)
- `search`: Search term for name, description, or owner
- `type`: Filter by type (all, borrow, share)

**Response:**
```json
{
    "items": [
        {
            "id": 1,
            "name": "string",
            "description": "string",
            "qty": 1,
            "remaining_qty": 1,
            "unit": "string",
            "thumbnail_url": "string",
            "photo_url": "string",
            "type": "borrow|share",
            "status": "available|borrowed",
            "owner": {
                "id": 1,
                "username": "string",
                "name": "string",
                "address": "string"
            }
        }
    ],
    "pagination": {
        "current_page": 1,
        "total_pages": 10,
        "total_items": 250,
        "items_per_page": 25
    }
}
```

#### POST /items/{item_id}/request
Request to borrow a specific item.

**Request Body:**
```json
{
    "requested_qty": 1,
    "date_start": "YYYY-MM-DD",
    "date_end": "YYYY-MM-DD"
}
```

### User Items (CRUD)

#### GET /user/items
Get all items owned by the current user.

#### POST /user/items
Create a new item listing.

**Request (multipart/form-data):**
- `name`: Item name
- `description`: Item description
- `qty`: Total quantity
- `unit`: Unit (pcs, kg, etc.)
- `type`: borrow|share
- `status`: available|borrowed
- `photo`: Image file (optional)

#### PUT /user/items/{item_id}
Update an existing item (owner only).

**Request (multipart/form-data):** Same as create

#### DELETE /user/items/{item_id}
Delete an item (owner only, no active requests).

### User Requests

#### GET /user/requests
Get requests for items.

**Query Parameters:**
- `type`: incoming (requests for your items) | outgoing (your requests)

#### PATCH /user/requests/{request_id}
Update request status.

**Request Body:**
```json
{
    "status": "approved|rejected|cancelled|returned"
}
```

**Status Transitions:**
- Owner can: approve, reject, returned
- Requester can: cancel
- pending → approved (owner)
- pending → rejected (owner)
- pending → cancelled (requester)
- approved → returned (owner)

### AI Recipe Generator

#### POST /ai/recipe
Generate recipe using AI.

**Request Body:**
```json
{
    "ingredients": "tomatoes, onions, garlic, pasta"
}
```

**Response:**
```json
{
    "recipe": {
        "title": "string",
        "ingredients": ["string"],
        "instructions": ["string"],
        "cooking_time": "string",
        "servings": "string",
        "difficulty": "easy|medium|hard"
    },
    "generated_at": "ISO datetime",
    "model": "string"
}
```

#### GET /ai/request/{request_id}/status
Get status of AI request.

#### GET /ai/requests/active
Get all active AI requests for current user.

#### DELETE /ai/request/{request_id}
Cancel an active AI request.

#### GET /ai/metrics
Get AI service performance metrics.

#### GET /ai/observers/status
Get AI observers status and events.

## Error Responses

All errors return JSON format:

```json
{
    "detail": "Error message description"
}
```

**Common HTTP Status Codes:**
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 500: Internal Server Error
- 503: Service Unavailable

## Data Models

### Item Types
- `borrow`: Item available for borrowing
- `share`: Item available for sharing

### Item Status
- `available`: Item can be requested
- `borrowed`: Item currently borrowed

### Request Status
- `pending`: Waiting for approval
- `approved`: Request approved
- `rejected`: Request rejected
- `cancelled`: Request cancelled
- `returned`: Item returned

## Postman Setup

1. **Import Collection:**
   - Open Postman
   - Click "Import" → "Link" → "Paste the URL or select file"
   - Choose `postman-collection.json`

2. **Import Environment:**
   - Go to "Environments" tab
   - Click "Import" → Select `postman-environment.json`
   - Set the environment as active

3. **Configure Variables:**
   - `base_url`: Set to your API server URL (default: http://localhost:8000)
   - `access_token`: Will be auto-filled after login
   - `item_id`: Set to a valid item ID for testing
   - `request_id`: Set to a valid request ID for testing

4. **Authentication Flow:**
   - First call "Register" or "Login" endpoint
   - The access token will be automatically stored
   - Subsequent requests will use the stored token

## WebSocket Support

Real-time notifications are available via WebSocket when enabled:
- Endpoint: `/ws/notifications/{user_id}`
- Events: New requests, status updates, AI request completion

## File Uploads

Item photos are uploaded to `/media/items/` directory:
- Supported formats: JPG, PNG, GIF, etc.
- Thumbnails are automatically generated (300x300)
- URLs are served from `/media/items/{filename}`

## Environment Configuration

Required environment variables:
- `OLLAMA_API_URL`: Ollama API endpoint for AI features
- `DEFAULT_OLLAMA_MODEL`: Default AI model name
- `ENABLE_NOTIFICATIONS`: Enable WebSocket notifications (default: true)
- `CORS_ALLOWED_ORIGINS`: Comma-separated list of allowed origins

## Testing

Use the provided Postman collection for comprehensive API testing. The collection includes:
- Authentication flows
- CRUD operations for items
- Request management
- AI recipe generation
- Error scenarios

## Rate Limiting

Currently not implemented, but consider adding:
- Login attempts
- AI recipe generation requests
- File upload limits

## Security Notes

- Passwords are hashed using bcrypt
- JWT tokens have 1-hour expiration
- Refresh tokens should be stored securely
- File uploads are validated for type and size
- CORS is configured for allowed origins
