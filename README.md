# ComKit

ComKit is a community kitchen sharing platform that allows users to borrow and share kitchen items within their community. This platform helps reduce waste and promote resource sharing among neighbors.

## POSTMAN collection

You can download the postman collection in this [postman link](https://www.postman.com/mission-candidate-28241265/workspace/comkit)

## Database Setup

If you want to create database, please run `python server_fastapi.migration`

This command will create the SQLite database with all necessary tables including users, items, and requests. The database file will be created in the server-fastapi directory.
Don't forget to setuup your `.env` too.

## Fake Data Generation

To populate the database with test data, use the `run_faker.py` script:

```bash
# Create 10 fake users
python server_fastapi.run_faker --users 10

# Create 20 fake items
python server_fastapi.run_faker --items 20

# Create 15 fake requests
python server_fastapi.run_faker --requests 15

# Create all fake data at once (10 users, 20 items, 15 requests)
python server_fastapi.run_faker --all

# Clear all data from database
python server_fastapi.run_faker --clear

# Custom numbers
python server_fastapi.run_faker --users 5 --items 10 --requests 8
```

Available options:
- `--users N`: Create N fake users (default: 10)
- `--items N`: Create N fake items (default: 20)
- `--requests N`: Create N fake requests (default: 15)
- `--all`: Create all fake data with default numbers
- `--clear`: Clear all data from database

## Running the Application

To start the ComKit FastAPI server, navigate to the project root directory and run the following command:

```bash
python -m server_fastapi.main
```

This command will start the FastAPI development server which typically runs on http://127.0.0.1:8000 by default. The server will automatically reload when you make changes to the source code, making it perfect for development and testing purposes. Make sure you have already set up your database using the migration script and optionally populated it with test data using the faker script before starting the application.
