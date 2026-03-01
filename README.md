# ComKit

<img width="1600" height="710" alt="LogoPPL" src="https://github.com/user-attachments/assets/074ed03e-c9c0-433f-8733-4b1a4802c243" />
ComKit is a community kitchen sharing platform that allows users to borrow and share kitchen items within their community. This platform helps reduce waste and promote resource sharing among neighbors.

## POSTMAN collection

You can download the postman collection in this [postman link](https://www.postman.com/mission-candidate-28241265/workspace/comkit)

## Database Setup

If you want to create database, please run `python server-fastapi/migration.py`

This command will create the SQLite database with all necessary tables including users, items, and requests. The database file will be created in the server-fastapi directory.
Don't forget to setuup your `.env` too.

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
