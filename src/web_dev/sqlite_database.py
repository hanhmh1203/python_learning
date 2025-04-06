"""
SQLite Database Management in Python

This module demonstrates SQLite database operations in Python, including:
- Database creation and connection
- Table creation and management
- Basic CRUD operations (Create, Read, Update, Delete)
- Using parameterized queries for security
"""

import sqlite3
import os
from datetime import datetime

# ===============================
# DATABASE SETUP AND CONNECTION
# ===============================

def create_connection(db_file="example.db"):
    """
    Create a connection to an SQLite database.
    Creates the database file if it doesn't exist.
    
    Args:
        db_file (str): Path to the database file
        
    Returns:
        sqlite3.Connection: Database connection object or None on error
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(db_file) or '.', exist_ok=True)
        
        # Connect to the database (will create it if it doesn't exist)
        conn = sqlite3.connect(db_file)
        
        # Enable foreign key constraints
        conn.execute("PRAGMA foreign_keys = ON")
        
        # Set row_factory to access columns by name
        conn.row_factory = sqlite3.Row
        
        print(f"Connected to SQLite database: {db_file}")
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# ===============================
# TABLE CREATION AND MANAGEMENT
# ===============================

def create_tables(conn):
    """
    Create the necessary tables for our example.
    
    Args:
        conn (sqlite3.Connection): Database connection
    """
    try:
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create posts table with foreign key reference to users
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
        ''')
        
        conn.commit()
        print("Tables created successfully")
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

# ===============================
# BASIC SQL OPERATIONS (CRUD)
# ===============================

# CREATE - Insert operations

def insert_user(conn, username, email):
    """
    Insert a new user into the users table.
    
    Args:
        conn (sqlite3.Connection): Database connection
        username (str): User's username
        email (str): User's email
        
    Returns:
        int: ID of the newly created user, or None on error
    """
    try:
        cursor = conn.cursor()
        
        # Use parameterized query to prevent SQL injection
        cursor.execute(
            "INSERT INTO users (username, email) VALUES (?, ?)",
            (username, email)
        )
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        print(f"Error: Username '{username}' already exists")
        return None
    except sqlite3.Error as e:
        print(f"Error inserting user: {e}")
        return None

def insert_post(conn, user_id, title, content):
    """
    Insert a new post for a user.
    
    Args:
        conn (sqlite3.Connection): Database connection
        user_id (int): ID of the user making the post
        title (str): Post title
        content (str): Post content
        
    Returns:
        int: ID of the newly created post, or None on error
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (user_id, title, content) VALUES (?, ?, ?)",
            (user_id, title, content)
        )
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.Error as e:
        print(f"Error inserting post: {e}")
        return None

# READ - Select operations

def get_all_users(conn):
    """
    Retrieve all users from the database.
    
    Args:
        conn (sqlite3.Connection): Database connection
        
    Returns:
        list: List of user dictionaries
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error retrieving users: {e}")
        return []

def get_user_by_id(conn, user_id):
    """
    Retrieve a user by their ID.
    
    Args:
        conn (sqlite3.Connection): Database connection
        user_id (int): User ID to retrieve
        
    Returns:
        dict: User data as a dictionary, or None if not found
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        return dict(user) if user else None
    except sqlite3.Error as e:
        print(f"Error retrieving user: {e}")
        return None

def get_posts_by_user(conn, user_id):
    """
    Retrieve all posts by a specific user.
    
    Args:
        conn (sqlite3.Connection): Database connection
        user_id (int): User ID to retrieve posts for
        
    Returns:
        list: List of post dictionaries
    """
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM posts WHERE user_id = ?", (user_id,))
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error retrieving posts: {e}")
        return []

# UPDATE operations

def update_user_email(conn, user_id, new_email):
    """
    Update a user's email address.
    
    Args:
        conn (sqlite3.Connection): Database connection
        user_id (int): User ID to update
        new_email (str): New email address
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET email = ? WHERE id = ?",
            (new_email, user_id)
        )
        conn.commit()
        
        # Check if any row was affected
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error updating user: {e}")
        return False

def update_post(conn, post_id, title=None, content=None):
    """
    Update a post's title and/or content.
    
    Args:
        conn (sqlite3.Connection): Database connection
        post_id (int): Post ID to update
        title (str, optional): New title
        content (str, optional): New content
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        update_parts = []
        params = []
        
        # Build dynamic SQL based on provided parameters
        if title is not None:
            update_parts.append("title = ?")
            params.append(title)
            
        if content is not None:
            update_parts.append("content = ?")
            params.append(content)
            
        if not update_parts:
            print("No updates specified")
            return False
            
        # Add the post_id to parameters
        params.append(post_id)
        
        # Execute the update
        query = f"UPDATE posts SET {', '.join(update_parts)} WHERE id = ?"
        cursor.execute(query, params)
        conn.commit()
        
        # Check if any row was affected
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error updating post: {e}")
        return False

# DELETE operations

def delete_user(conn, user_id):
    """
    Delete a user from the database.
    Due to foreign key constraints, this will also delete all the user's posts.
    
    Args:
        conn (sqlite3.Connection): Database connection
        user_id (int): User ID to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        
        # Check if any row was affected
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting user: {e}")
        return False

def delete_post(conn, post_id):
    """
    Delete a post from the database.
    
    Args:
        conn (sqlite3.Connection): Database connection
        post_id (int): Post ID to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        
        # Check if any row was affected
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting post: {e}")
        return False

# ===============================
# ADVANCED QUERIES
# ===============================

def get_user_with_posts_count(conn):
    """
    Get all users with a count of how many posts they've made.
    Demonstrates a JOIN operation.
    
    Args:
        conn (sqlite3.Connection): Database connection
        
    Returns:
        list: List of dictionaries with user data and post count
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                u.id, u.username, u.email, COUNT(p.id) as post_count
            FROM 
                users u
            LEFT JOIN 
                posts p ON u.id = p.user_id
            GROUP BY 
                u.id
        """)
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error retrieving user post counts: {e}")
        return []

def search_posts_by_keyword(conn, keyword):
    """
    Search for posts containing a specific keyword.
    Demonstrates text search in SQLite.
    
    Args:
        conn (sqlite3.Connection): Database connection
        keyword (str): Keyword to search for
        
    Returns:
        list: List of matching post dictionaries
    """
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                p.id, p.title, p.content, p.published_at, 
                u.username as author
            FROM 
                posts p
            JOIN 
                users u ON p.user_id = u.id
            WHERE 
                p.title LIKE ? OR p.content LIKE ?
        """, (f'%{keyword}%', f'%{keyword}%'))
        return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        print(f"Error searching posts: {e}")
        return []

# ===============================
# PRACTICAL EXAMPLE
# ===============================

def run_demo():
    """Run a demonstration of all the SQLite operations."""
    # Create a connection to a new database
    conn = create_connection("demo.db")
    if not conn:
        return
        
    # Create tables
    create_tables(conn)
    
    # Create operations - Insert users
    print("\n=== Creating Users ===")
    user1_id = insert_user(conn, "john_doe", "john@example.com")
    user2_id = insert_user(conn, "jane_smith", "jane@example.com")
    
    if user1_id and user2_id:
        print(f"Created users with IDs: {user1_id}, {user2_id}")
        
        # Create operations - Insert posts
        print("\n=== Creating Posts ===")
        post1_id = insert_post(conn, user1_id, "Hello World", "My first blog post!")
        post2_id = insert_post(conn, user1_id, "SQLite Tutorial", "SQLite is a great embedded database.")
        post3_id = insert_post(conn, user2_id, "Python Programming", "Python is awesome for data analysis.")
        
        if post1_id and post2_id and post3_id:
            print(f"Created posts with IDs: {post1_id}, {post2_id}, {post3_id}")
    
    # Read operations
    print("\n=== All Users ===")
    users = get_all_users(conn)
    for user in users:
        print(f"User ID: {user['id']}, Username: {user['username']}, Email: {user['email']}")
    
    if user1_id:
        print(f"\n=== Posts by User {user1_id} ===")
        posts = get_posts_by_user(conn, user1_id)
        for post in posts:
            print(f"Post ID: {post['id']}, Title: {post['title']}")
    
    # Update operations
    if user1_id:
        print("\n=== Updating User ===")
        if update_user_email(conn, user1_id, "john.doe@newemail.com"):
            updated_user = get_user_by_id(conn, user1_id)
            print(f"Updated user email: {updated_user['email']}")
    
    if post1_id:
        print("\n=== Updating Post ===")
        if update_post(conn, post1_id, content="Updated content for my first blog post!"):
            print(f"Successfully updated post {post1_id}")
    
    # Advanced queries
    print("\n=== Users with Post Counts ===")
    user_stats = get_user_with_posts_count(conn)
    for stat in user_stats:
        print(f"User: {stat['username']}, Posts: {stat['post_count']}")
    
    print("\n=== Posts Containing 'SQLite' ===")
    matching_posts = search_posts_by_keyword(conn, "SQLite")
    for post in matching_posts:
        print(f"Post: {post['title']} by {post['author']}")
    
    # Delete operations
    if post2_id:
        print("\n=== Deleting Post ===")
        if delete_post(conn, post2_id):
            print(f"Deleted post {post2_id}")
    
    if user2_id:
        print("\n=== Deleting User ===")
        if delete_user(conn, user2_id):
            print(f"Deleted user {user2_id} and all their posts")
    
    # Final user list
    print("\n=== Final User List ===")
    final_users = get_all_users(conn)
    for user in final_users:
        print(f"User ID: {user['id']}, Username: {user['username']}, Email: {user['email']}")
    
    # Close the connection
    conn.close()
    print("\nDatabase connection closed")

# Run the demo if this script is executed directly
if __name__ == "__main__":
    run_demo()