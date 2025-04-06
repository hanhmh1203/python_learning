"""
FastAPI Application with SQLite Integration

This file demonstrates building a RESTful API with FastAPI and SQLite,
implementing CRUD operations for a simple user management system.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr, Field
import sqlite3
from typing import List, Optional
import uvicorn

# Initialize FastAPI application
app = FastAPI(
    title="User Management API",
    description="A RESTful API for managing users built with FastAPI and SQLite",
    version="1.0.0"
)

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
# DATA MODELS (PYDANTIC MODELS)
# ==============================

class UserBase(BaseModel):
    """Base model with common user attributes."""
    username: str = Field(..., min_length=3, max_length=50, example="johndoe")
    email: EmailStr = Field(..., example="john@example.com")
    age: Optional[int] = Field(None, ge=0, le=120, example=30)

class UserCreate(UserBase):
    """Model for creating a new user."""
    pass

class UserUpdate(BaseModel):
    """Model for updating a user (all fields optional)."""
    email: Optional[EmailStr] = Field(None, example="newemail@example.com")
    age: Optional[int] = Field(None, ge=0, le=120, example=31)

class User(UserBase):
    """Model for a user retrieved from the database."""
    id: int
    created_at: str
    
    class Config:
        """Configure Pydantic to work with ORM models."""
        orm_mode = True

# ==============================
# API ENDPOINTS (CRUD OPERATIONS)
# ==============================

# Create a new user (CREATE)
@app.post("/api/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user with the provided details.
    
    - **username**: Required - A unique username (3-50 characters)
    - **email**: Required - A valid email address
    - **age**: Optional - Age between 0-120
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, age) VALUES (?, ?, ?)",
            (user.username, user.email, user.age)
        )
        conn.commit()
        
        # Get the newly created user
        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        new_user = dict(cursor.fetchone())
        conn.close()
        
        return new_user
    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Username '{user.username}' already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get all users (READ)
@app.get("/api/users", response_model=List[User])
async def get_all_users():
    """Retrieve all users from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get a single user by ID (READ)
@app.get("/api/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """
    Retrieve a specific user by their ID.
    
    - **user_id**: The ID of the user to retrieve
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return dict(user)
    except HTTPException:
        raise  # Re-raise HTTPExceptions for proper error handling
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Update a user (UPDATE)
@app.put("/api/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """
    Update an existing user's information.
    
    - **user_id**: The ID of the user to update
    - **email**: Optional - New email address
    - **age**: Optional - New age between 0-120
    """
    # Check if any fields are provided for update
    update_data = user_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update"
        )
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if the user exists
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Build the dynamic part of the SQL query
        update_fields = []
        params = []
        
        if 'email' in update_data:
            update_fields.append("email = ?")
            params.append(update_data['email'])
        
        if 'age' in update_data:
            update_fields.append("age = ?")
            params.append(update_data['age'])
        
        # Complete the parameter list with the user_id
        params.append(user_id)
        
        # Perform the update
        query = f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        
        # Get the updated user
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        updated_user = dict(cursor.fetchone())
        conn.close()
        
        return updated_user
    except HTTPException:
        raise  # Re-raise HTTPExceptions for proper error handling
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Delete a user (DELETE)
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int):
    """
    Delete a user by their ID.
    
    - **user_id**: The ID of the user to delete
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if the user exists
        cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Delete the user
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        # Return no content on successful deletion
        return None
    except HTTPException:
        raise  # Re-raise HTTPExceptions for proper error handling
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ==============================
# JSON HANDLING
# ==============================

"""
FastAPI automatically handles JSON serialization and deserialization:

1. Serialization (Python → JSON):
   - Return Pydantic models or Python dictionaries directly
   - FastAPI uses Pydantic to validate and convert to JSON

2. Deserialization (JSON → Python):
   - Use Pydantic models as function parameters
   - FastAPI validates input data against the model schema
   - Type validation, conversion, and error handling are automatic

Advantages over Flask:
- Automatic validation with clear error messages
- Type conversion (strings to integers, etc.)
- Documentation generation from type hints and models
- OpenAPI schema generation for client code generation
"""

# ==============================
# MAIN APPLICATION ENTRYPOINT
# ==============================

if __name__ == '__main__':
    print("Starting FastAPI server...")
    print("API Documentation automatically available at:")
    print("- Swagger UI: http://127.0.0.1:8000/docs")
    print("- ReDoc: http://127.0.0.1:8000/redoc")
    
    # Start the FastAPI application with Uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)