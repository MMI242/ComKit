#!/bin/bash

# Script to run the FastAPI server

cd "$(dirname "$0")"

echo "Starting FastAPI server..."
echo "Server will run on http://localhost:8000"
echo "API docs: http://localhost:8000/docs"
echo ""

python main.py
