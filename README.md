# ComKit

<img width="1600" height="710" alt="LogoPPL" src="https://github.com/user-attachments/assets/074ed03e-c9c0-433f-8733-4b1a4802c243" />
ComKit is a community kitchen sharing platform that allows users to borrow and share kitchen items within their community. This platform helps reduce waste and promote resource sharing among neighbors.

## POSTMAN collection

You can download the postman collection in this [postman link](https://www.postman.com/mission-candidate-28241265/workspace/comkit)

## Database Setup

If you want to create database, please run `python server-fastapi/migration.py`

This command will create the SQLite database with all necessary tables including users, items, and requests. The database file will be created in the server-fastapi directory.
Don't forget to setup your `.env` too.

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

Available options:
- `--users N`: Create N fake users (default: 10)
- `--items N`: Create N fake items (default: 20)
- `--requests N`: Create N fake requests (default: 15)
- `--all`: Create all fake data with default numbers
- `--clear`: Clear all data from database
