# ComKit Frontend API Integration

This document describes how the frontend integrates with the FastAPI backend.

## API Configuration

The frontend is configured to connect to the FastAPI backend through the following:

1. **Environment Variables**:
   - `NUXT_PUBLIC_API_BASE`: Base URL for the API (default: http://localhost:8000)
   - `NUXT_PUBLIC_API_TIMEOUT`: API timeout in milliseconds (default: 10000)

2. **Configuration Files**:
   - `nuxt.config.ts`: Contains runtime configuration
   - `.env.example`: Example environment variables

## API Services

### Authentication Service (`~/services/api.ts`)

The API service provides:
- `authApi.login()`: Login with username/password
- `authApi.register()`: Register new user
- `authApi.refreshToken()`: Refresh access token

### Auth Composable (`~/composables/useAuth.ts`)

The auth composable manages authentication state:
- `login()`: Authenticate user and store tokens
- `register()`: Register and auto-login new user
- `logout()`: Clear auth state and redirect
- `isAuthenticated`: Computed property for auth status
- `currentUser`: Computed property for current user

## Token Storage

- **Remember Me = ON**: Tokens stored in localStorage
- **Remember Me = OFF**: Tokens stored in sessionStorage
- Tokens include: access_token, refresh_token, and user data

## API Endpoints

### Authentication
- `POST /auth/login` - Login user
- `POST /auth/register` - Register user
- `POST /auth/refresh` - Refresh access token

### Response Format

```typescript
interface AuthResponse {
  access_token: string
  refresh_token: string
  token_type: string
  expires_in: number
  user: {
    id: number
    username: string
    name: string
    address: string
  }
}
```

## Usage Example

```typescript
// Login
const { login } = useAuth()
try {
  await login('username', 'password', true) // remember me
  await navigateTo('/dashboard')
} catch (error) {
  console.error('Login failed:', error.detail)
}

// Check auth status
const { isAuthenticated, currentUser } = useAuth()
if (isAuthenticated.value) {
  console.log('Current user:', currentUser.value)
}
```

## Development Setup

1. Copy `.env.example` to `.env.local`
2. Set `NUXT_PUBLIC_API_BASE=http://localhost:8000`
3. Start the FastAPI server: `cd server-fastapi && python main.py`
4. Start the Nuxt dev server: `cd ui && npm run dev`

## Testing

The login functionality is tested in:
- `test/pages/login.test.ts` - Comprehensive login tests
- Tests mock the `useAuth` composable and API calls
