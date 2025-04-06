"""
Flask Application with SQLite Integration

This file demonstrates building a RESTful API with Flask and SQLite,
implementing CRUD operations for a simple user management system.
"""

from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Database setup and helper functions
DB_PATH = 'users.db'

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def init_db():
    """Initialize the database with the users table if it doesn't exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Initialize the database when this module is imported
init_db()

# ==============================
# API ENDPOINTS (CRUD OPERATIONS)
# ==============================

# Create a new user (CREATE)
@app.route('/api/users', methods=['POST'])
def create_user():
    """
    Create a new user with the provided details.
    
    Expected JSON payload:
    {
        "username": "johndoe",
        "email": "john@example.com",
        "age": 30
    }
    """
    data = request.get_json()
    
    # Validate required fields
    if not all(key in data for key in ('username', 'email')):
        return jsonify({"error": "Username and email are required"}), 400
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
            (data['username'], data['email'], data.get('age'))
        )
        conn.commit()
        
        # Get the ID of the newly created user
        user_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "message": "User created successfully",
            "user_id": user_id
        }), 201
        
    except sqlite3.IntegrityError:
        return jsonify({"error": f"Username '{data['username']}' already exists"}), 409
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get all users (READ)
@app.route('/api/users', methods=['GET'])
def get_all_users():
    """Retrieve all users from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({"users": users}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get a single user by ID (READ)
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a specific user by their ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            return jsonify({"user": dict(user)}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Update a user (UPDATE)
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user's information.
    
    Expected JSON payload:
    {
        "email": "newemail@example.com",
        "age": 31
    }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "No data provided for update"}), 400
    
    # Build the dynamic part of the SQL query
    update_fields = []
    params = []
    
    if 'email' in data:
        update_fields.append("email = ?")
        params.append(data['email'])
    
    if 'age' in data:
        update_fields.append("age = ?")
        params.append(data['age'])
    
    if not update_fields:
        return jsonify({"error": "No valid fields to update"}), 400
    
    # Complete the parameter list with the user_id
    params.append(user_id)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if the user exists
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        # Perform the update
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        conn.close()
        
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a user (DELETE)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by their ID."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if the user exists
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        # Delete the user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ==============================
# JSON HANDLING
# ==============================

"""
Flask automatically handles JSON serialization and deserialization:

1. Serialization (Python → JSON):
   - Use jsonify() to convert Python dictionaries to JSON responses
   - Example: return jsonify({"name": "John", "age": 30})

2. Deserialization (JSON → Python):
   - Use request.get_json() to parse JSON from request bodies
   - Example: data = request.get_json()
"""

# ==============================
# MAIN APPLICATION ENTRYPOINT
# ==============================

if __name__ == '__main__':
    print("Starting Flask API server...")
    print("API Documentation:")
    print("- POST /api/users - Create a new user")
    print("- GET /api/users - Get all users")
    print("- GET /api/users/<id> - Get a specific user")
    print("- PUT /api/users/<id> - Update a user")
    print("- DELETE /api/users/<id> - Delete a user")
    
    # Start the Flask application in debug mode
    app.run(debug=True)