"""
FastAPI Application with SQLite Integration for Quotes Management

This file implements a RESTful API with FastAPI and SQLite,
providing CRUD operations for a quotes management system with favorite functionality.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
import sqlite3
from typing import List, Optional, Dict
import uvicorn
from datetime import datetime
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI application
app = FastAPI(
    title="Quotes API",
    description="A RESTful API for managing quotes with favorite functionality, built with FastAPI and SQLite",
    version="1.0.0"
)

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (you may want to restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Database setup and helper functions
# Check if running in Fly.io environment and use the mounted volume
if os.path.exists('/app/data'):
    DB_PATH = '/app/data/quotes.db'
    print(f"Using database at {DB_PATH}")
else:
    DB_PATH = 'quotes.db'
    print(f"Using local database at {DB_PATH}")

def get_db_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']
    return conn

def init_db():
    """Initialize the database with the necessary tables if they don't exist."""
    # Create data directory if it doesn't exist and we're in Fly.io environment
    if os.path.exists('/app') and not os.path.exists('/app/data'):
        os.makedirs('/app/data', exist_ok=True)
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create quotes table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quotes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        author TEXT NOT NULL,
        source TEXT,
        category TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create favorites table with user_id to track which user favorited which quote
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS favorites (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quote_id INTEGER NOT NULL,
        user_id TEXT NOT NULL,  /* This could be a device ID or actual user ID */
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(quote_id, user_id),
        FOREIGN KEY (quote_id) REFERENCES quotes (id) ON DELETE CASCADE
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

class QuoteBase(BaseModel):
    """Base model with common quote attributes."""
    text: str = Field(..., min_length=1, example="The journey of a thousand miles begins with a single step.")
    author: str = Field(..., example="Lao Tzu")
    source: Optional[str] = Field(None, example="Tao Te Ching")
    category: Optional[str] = Field(None, example="Philosophy")

class QuoteCreate(QuoteBase):
    """Model for creating a new quote."""
    pass

class QuoteUpdate(BaseModel):
    """Model for updating a quote (all fields optional)."""
    text: Optional[str] = Field(None, example="Updated quote text")
    author: Optional[str] = Field(None, example="Updated author")
    source: Optional[str] = Field(None, example="Updated source")
    category: Optional[str] = Field(None, example="Updated category")

class Quote(QuoteBase):
    """Model for a quote retrieved from the database."""
    id: int
    created_at: str
    is_favorite: bool = False  # Will be set when retrieving quotes
    
    class Config:
        """Configure Pydantic to work with ORM models."""
        from_attributes = True

class FavoriteCreate(BaseModel):
    """Model for marking a quote as favorite."""
    user_id: str = Field(..., example="user123")

class Favorite(BaseModel):
    """Model for favorite information."""
    id: int
    quote_id: int
    user_id: str
    created_at: str

# ==============================
# API ENDPOINTS (CRUD OPERATIONS)
# ==============================

# Create a new quote (CREATE)
@app.post("/api/quotes", response_model=Quote, status_code=status.HTTP_201_CREATED)
async def create_quote(quote: QuoteCreate):
    """
    Create a new quote with the provided details.
    
    - **text**: Required - The quote text
    - **author**: Required - The author of the quote
    - **source**: Optional - Source of the quote (book, speech, etc.)
    - **category**: Optional - Category or theme of the quote
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO quotes (text, author, source, category) VALUES (?, ?, ?, ?)",
            (quote.text, quote.author, quote.source, quote.category)
        )
        conn.commit()
        
        # Get the newly created quote
        quote_id = cursor.lastrowid
        cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
        new_quote = dict(cursor.fetchone())
        new_quote["is_favorite"] = False  # New quote is not a favorite by default
        conn.close()
        
        return new_quote
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Create multiple quotes at once (BATCH CREATE)
@app.post("/api/quotes/batch", response_model=List[Quote], status_code=status.HTTP_201_CREATED)
async def create_quotes_batch(quotes: List[QuoteCreate]):
    """
    Create multiple quotes at once with the provided details.
    
    - **quotes**: Required - A list of quotes to create
    
    Each quote in the list requires:
    - **text**: Required - The quote text
    - **author**: Required - The author of the quote
    - **source**: Optional - Source of the quote (book, speech, etc.)
    - **category**: Optional - Category or theme of the quote
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        created_quotes = []
        
        for quote in quotes:
            cursor.execute(
                "INSERT INTO quotes (text, author, source, category) VALUES (?, ?, ?, ?)",
                (quote.text, quote.author, quote.source, quote.category)
            )
            
            # Get the newly created quote
            quote_id = cursor.lastrowid
            cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
            new_quote = dict(cursor.fetchone())
            new_quote["is_favorite"] = False  # New quote is not a favorite by default
            created_quotes.append(new_quote)
        
        conn.commit()
        conn.close()
        
        return created_quotes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get all quotes (READ)
@app.get("/api/quotes", response_model=List[Quote])
async def get_all_quotes(user_id: Optional[str] = None):
    """
    Retrieve all quotes from the database.
    
    - **user_id**: Optional - If provided, will mark quotes as favorites for this user
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes")
        quotes = [dict(row) for row in cursor.fetchall()]
        
        # If user_id is provided, mark quotes as favorites for this user
        if user_id:
            cursor.execute(
                "SELECT quote_id FROM favorites WHERE user_id = ?", 
                (user_id,)
            )
            favorite_quote_ids = {row[0] for row in cursor.fetchall()}
            
            for quote in quotes:
                quote["is_favorite"] = quote["id"] in favorite_quote_ids
        else:
            # Set is_favorite to false for all quotes when no user_id provided
            for quote in quotes:
                quote["is_favorite"] = False
                
        conn.close()
        
        return quotes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get a single quote by ID (READ)
@app.get("/api/quotes/{quote_id}", response_model=Quote)
async def get_quote(quote_id: int, user_id: Optional[str] = None):
    """
    Retrieve a specific quote by its ID.
    
    - **quote_id**: The ID of the quote to retrieve
    - **user_id**: Optional - If provided, will check if the quote is a favorite for this user
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
        quote = cursor.fetchone()
        
        if not quote:
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quote not found"
            )
        
        result = dict(quote)
        
        # Check if this quote is a favorite for the user
        if user_id:
            cursor.execute(
                "SELECT 1 FROM favorites WHERE quote_id = ? AND user_id = ?", 
                (quote_id, user_id)
            )
            result["is_favorite"] = cursor.fetchone() is not None
        else:
            result["is_favorite"] = False
            
        conn.close()
        
        return result
    except HTTPException:
        raise  # Re-raise HTTPExceptions for proper error handling
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Update a quote (UPDATE)
@app.put("/api/quotes/{quote_id}", response_model=Quote)
async def update_quote(quote_id: int, quote_update: QuoteUpdate, user_id: Optional[str] = None):
    """
    Update an existing quote's information.
    
    - **quote_id**: The ID of the quote to update
    - **text**: Optional - New quote text
    - **author**: Optional - New author
    - **source**: Optional - New source
    - **category**: Optional - New category
    - **user_id**: Optional - If provided, will check if the quote is a favorite for this user
    """
    # Check if any fields are provided for update
    update_data = quote_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No valid fields to update"
        )
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if the quote exists
        cursor.execute("SELECT 1 FROM quotes WHERE id = ?", (quote_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quote not found"
            )
        
        # Build the dynamic part of the SQL query
        update_fields = []
        params = []
        
        for field, value in update_data.items():
            update_fields.append(f"{field} = ?")
            params.append(value)
        
        # Complete the parameter list with the quote_id
        params.append(quote_id)
        
        # Perform the update
        query = f"UPDATE quotes SET {', '.join(update_fields)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        
        # Get the updated quote
        cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
        updated_quote = dict(cursor.fetchone())
        
        # Check if this quote is a favorite for the user
        if user_id:
            cursor.execute(
                "SELECT 1 FROM favorites WHERE quote_id = ? AND user_id = ?", 
                (quote_id, user_id)
            )
            updated_quote["is_favorite"] = cursor.fetchone() is not None
        else:
            updated_quote["is_favorite"] = False
            
        conn.close()
        
        return updated_quote
    except HTTPException:
        raise  # Re-raise HTTPExceptions for proper error handling
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Delete a quote (DELETE)
@app.delete("/api/quotes/{quote_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quote(quote_id: int):
    """
    Delete a quote by its ID.
    
    - **quote_id**: The ID of the quote to delete
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if the quote exists
        cursor.execute("SELECT 1 FROM quotes WHERE id = ?", (quote_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quote not found"
            )
        
        # Delete the quote (this will also delete related favorites due to the CASCADE constraint)
        cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
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
# FAVORITE MANAGEMENT ENDPOINTS
# ==============================

# Mark a quote as favorite
@app.post("/api/quotes/{quote_id}/favorite", response_model=Dict[str, bool])
async def add_favorite(quote_id: int, favorite: FavoriteCreate):
    """
    Mark a quote as favorite for a specific user.
    
    - **quote_id**: The ID of the quote to mark as favorite
    - **user_id**: The ID of the user marking the quote as favorite
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # First check if the quote exists
        cursor.execute("SELECT 1 FROM quotes WHERE id = ?", (quote_id,))
        if not cursor.fetchone():
            conn.close()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Quote not found"
            )
        
        # Add to favorites if not already a favorite
        try:
            cursor.execute(
                "INSERT INTO favorites (quote_id, user_id) VALUES (?, ?)",
                (quote_id, favorite.user_id)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            # Already a favorite, not an error
            pass
            
        conn.close()
        
        return {"success": True}
    except HTTPException:
        raise  # Re-raise HTTPExceptions for proper error handling
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Remove a quote from favorites
@app.delete("/api/quotes/{quote_id}/favorite", response_model=Dict[str, bool])
async def remove_favorite(quote_id: int, user_id: str):
    """
    Remove a quote from a user's favorites.
    
    - **quote_id**: The ID of the quote to remove from favorites
    - **user_id**: The ID of the user removing the favorite
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Delete the favorite entry
        cursor.execute(
            "DELETE FROM favorites WHERE quote_id = ? AND user_id = ?",
            (quote_id, user_id)
        )
        conn.commit()
        
        # Check if any rows were affected
        success = cursor.rowcount > 0
        conn.close()
        
        return {"success": success}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get all favorite quotes for a user
@app.get("/api/favorites", response_model=List[Quote])
async def get_favorite_quotes(user_id: str):
    """
    Retrieve all quotes marked as favorite by a specific user.
    
    - **user_id**: The ID of the user whose favorites to retrieve
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get all quotes that are favorites for this user
        cursor.execute("""
            SELECT q.* FROM quotes q
            JOIN favorites f ON q.id = f.quote_id
            WHERE f.user_id = ?
        """, (user_id,))
        
        quotes = [dict(row) for row in cursor.fetchall()]
        
        # Mark all retrieved quotes as favorites
        for quote in quotes:
            quote["is_favorite"] = True
            
        conn.close()
        
        return quotes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# ==============================
# CATEGORY MANAGEMENT ENDPOINTS
# ==============================

# Get all quote categories
@app.get("/api/categories", response_model=List[str])
async def get_categories():
    """Retrieve all unique quote categories from the database."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM quotes WHERE category IS NOT NULL")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

# Get quotes by category
@app.get("/api/quotes/category/{category}", response_model=List[Quote])
async def get_quotes_by_category(category: str, user_id: Optional[str] = None):
    """
    Retrieve all quotes in a specific category.
    
    - **category**: The category to filter quotes by
    - **user_id**: Optional - If provided, will mark quotes as favorites for this user
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes WHERE category = ?", (category,))
        quotes = [dict(row) for row in cursor.fetchall()]
        
        # If user_id is provided, mark quotes as favorites for this user
        if user_id:
            cursor.execute(
                "SELECT quote_id FROM favorites WHERE user_id = ?", 
                (user_id,)
            )
            favorite_quote_ids = {row[0] for row in cursor.fetchall()}
            
            for quote in quotes:
                quote["is_favorite"] = quote["id"] in favorite_quote_ids
        else:
            # Set is_favorite to false for all quotes when no user_id provided
            for quote in quotes:
                quote["is_favorite"] = False
                
        conn.close()
        
        return quotes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

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