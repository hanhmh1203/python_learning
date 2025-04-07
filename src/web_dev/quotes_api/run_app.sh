#!/bin/bash

# Script to run the Quotes API FastAPI application with the correct environment

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="/Volumes/SN770/source code/python/proj1"

echo "Activating virtual environment..."
source "$PROJECT_DIR/venv/bin/activate"

echo "Installing required packages if needed..."
pip install fastapi uvicorn pydantic email-validator

echo "Starting Quotes API application..."
cd "$SCRIPT_DIR"

# Run FastAPI app with uvicorn
# The $PORT environment variable is set by Fly.io
PORT="${PORT:-8000}"
uvicorn app:app --host 0.0.0.0 --port $PORT

# This script will deactivate the virtual environment automatically when it exits