# ComKit

<img width="1600" height="710" alt="LogoPPL" src="https://github.com/user-attachments/assets/074ed03e-c9c0-433f-8733-4b1a4802c243" />
ComKit is a community kitchen sharing platform that allows users to borrow and share kitchen items within their community. This platform helps reduce waste and promote resource sharing among neighbors.

## Quickstart
To reproduce application, it's recommended to use use docker 
1. clone the repo, cd to cloned directory
2. copy ui/.env.example to `ui/.env` and server-fastapi/.env.example to `server-fastapi/.env`, and edit as necessary.

   Note: to use cloud ollama (https://ollama.com/):
   - register https://ollama.com/
   - settings -> keys -> add API key, copy to server-fastapi/.env as `OLLAMA_API_KEY=`
   - specify cloud-only model in server-fastapi/.env (recommended model is `DEFAULT_OLLAMA_MODEL=qwen3.5:cloud`)
   - specify `OLLAMA_API_URL=https://ollama.com/`
4. docker compose up -d
5. frontend will be served in http://localhost:8001/login by default (see docker-compose.yaml)

## API Documentation

### Interactive Documentation
Start the backend server and visit:
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API testing
- **ReDoc**: `http://localhost:8000/redoc` - Clean API documentation

### Postman Collection
For API testing, you can:
1. Import the local Postman collection: `postman-collection.json`
2. Import the environment: `postman-environment.json`
3. Or view the online collection: [Postman Workspace](https://www.postman.com/mission-candidate-28241265/workspace/comkit)

### API Reference
See `API_DOCUMENTATION.md` for complete API reference with examples, authentication flows, and integration guides.

## Database Setup

If you want to create database, please run `python server-fastapi/migration.py`

This command will create the SQLite database with all necessary tables including users, items, and requests. The database file will be created in the server-fastapi directory.
Don't forget to setup your `.env` too.

## Backend (FastAPI) Setup and Running

### Prerequisites
- Python 3.8 or higher
- pip

### Installation

1. Navigate to the server directory:
```bash
cd server-fastapi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Environment Setup:
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
# Set up database URL, Ollama API for AI features, etc.
```

### Running the Development Server

1. Start the backend server:
```bash
python main.py
```

2. The API will be available at:
```
http://localhost:8000
```

3. Interactive API documentation:
```
http://localhost:8000/docs
```

### Available Scripts
- `python main.py` - Start development server
- `python migration.py` - Create database tables
- `python run_faker.py` - Generate fake data for testing

### Features
- JWT Authentication with refresh tokens
- RESTful API with OpenAPI documentation
- File upload support for item photos
- AI-powered recipe generation (Ollama)
- WebSocket notifications
- SQLite database with SQLAlchemy

## Frontend (Nuxt UI) Setup and Running

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. Navigate to the UI directory:
```bash
cd ui
```

2. Install dependencies:
```bash
# Using npm
npm install

# Or using yarn
yarn install
```

3. Environment Setup:
```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your configuration
# Make sure to set the correct API URL for your backend
```

### Running the Development Server

1. Start the development server:
```bash
# Using npm
npm run dev

# Or using yarn
yarn dev
```

2. The application will be available at:
```
http://localhost:3000
```

### Available Scripts

- `npm run dev` - Start development server with hot reload
- `npm run build` - Build for production
- `npm run generate` - Generate static site
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run typecheck` - Run TypeScript type checking

### Important Notes

- Make sure the backend server is running on `http://localhost:8000` before starting the frontend
- The frontend is configured to use HTTP-only cookies for authentication
- CORS is properly configured between frontend (port 3000) and backend (port 8000)

## Fake Data Generation

To populate the database with test data, use the `run_faker.py` script:

```bash
# Create 10 fake users
python server-fastapi/run_faker.py --users 10

# Create 20 fake items
python server-fastapi/run_faker.py --items 20

# Create 15 fake requests
python server-fastapi/run_faker.py --requests 15

# Create all fake data at once (10 users, 20 items, 15 requests)
python server-fastapi/run_faker.py --all

# Clear all data from database
python server-fastapi/run_faker.py --clear

# Custom numbers
python server-fastapi/run_faker.py --users 5 --items 10 --requests 8
```

## Project Structure

```
ComKit/
├── server-fastapi/          # Backend API (FastAPI)
│   ├── main.py             # Main application entry point
│   ├── models.py           # Database models
│   ├── schemas.py          # Pydantic schemas
│   ├── auth.py             # Authentication logic
│   ├── routes_*.py         # API route handlers
│   ├── migration.py        # Database migration
│   └── run_faker.py        # Fake data generator
├── ui/                     # Frontend (Nuxt.js)
│   ├── pages/              # Vue pages
│   ├── components/         # Vue components
│   ├── composables/        # Vue composables
│   └── assets/             # Static assets
├── docs/                   # Project documentation
├── postman-collection.json # API collection for testing
├── postman-environment.json # Environment variables
└── API_DOCUMENTATION.md    # Complete API reference
```

## Key Features

### 🏪 Item Sharing
- List kitchen items for borrowing or sharing
- Search and filter available items
- Photo uploads with thumbnails
- Item status management

### 🔐 Authentication
- JWT-based authentication
- Refresh token support
- HTTP-only cookie security
- User registration and login

### 🤝 Request System
- Borrowing requests with date ranges
- Approval workflows
- Status tracking (pending, approved, returned)
- Real-time notifications

### 🤖 AI Integration
- Recipe generation based on available ingredients
- Ollama AI integration
- Request tracking and metrics
- Observer pattern for monitoring

### 📱 Modern UI
- Responsive Nuxt.js frontend
- Real-time updates
- File upload support
- Clean, intuitive interface

## Development Workflow

1. **Setup Database**: `python server-fastapi/migration.py`
2. **Start Backend**: `cd server-fastapi && python main.py`
3. **Start Frontend**: `cd ui && npm run dev`
4. **Visit App**: `http://localhost:3000`
5. **API Docs**: `http://localhost:8000/docs`

## Testing

### Backend Testing
```bash
cd test-server
python test_login.py
python test_register.py
python test_user_items.py
```

### Frontend Testing
```bash
cd ui
npm run test
```

### API Testing
Import `postman-collection.json` into Postman or use the interactive Swagger UI.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
