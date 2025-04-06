"""
Web Frameworks Comparison: Flask vs. FastAPI

This file provides a comparison of Flask and FastAPI, two popular Python web frameworks,
along with examples demonstrating their basic usage.
"""

# ===============================
# INTRODUCTION TO WEB FRAMEWORKS
# ===============================

"""
Flask vs. FastAPI: Overview and Comparison

1. FLASK
   - Released in 2010, a lightweight "micro" framework
   - Built on Werkzeug WSGI toolkit and Jinja2 template engine
   - Synchronous by default (one request at a time)
   - Minimalist design philosophy with extensions for additional functionality

   Pros:
   - Simple and easy to learn
   - Great documentation and large community
   - Flexible with minimal constraints
   - Extensive ecosystem of extensions
   - Mature and stable

   Cons:
   - Synchronous by default (slower for I/O bound operations)
   - Requires additional libraries for features like validation
   - Less built-in functionality compared to full-stack frameworks

2. FASTAPI
   - Released in 2018, a modern, high-performance framework
   - Built on Starlette (ASGI framework) and Pydantic (data validation)
   - Asynchronous by default (multiple requests concurrently)
   - Strongly typed with Python type hints

   Pros:
   - Very high performance (one of the fastest Python frameworks)
   - Built-in data validation via Pydantic
   - Automatic API documentation (OpenAPI/Swagger)
   - Native async/await support
   - Type hints integration helps catch errors early
   - Modern design with good practices built-in

   Cons:
   - Newer with a smaller (but rapidly growing) community
   - Steeper learning curve for beginners
   - Requires understanding of async concepts for full benefits
   - May be overkill for very simple applications
"""

# Example dependencies that would be installed for each:
"""
For Flask:
pip install flask

For FastAPI:
pip install fastapi uvicorn
"""

# ===============================
# REST API DESIGN PRINCIPLES
# ===============================

"""
REST (Representational State Transfer) API Design Principles

1. Resource-based: Design around resources (nouns), not actions
   - Good: /users, /products
   - Avoid: /getUsers, /createProduct

2. HTTP Methods represent operations:
   - GET: Retrieve data (safe, idempotent)
   - POST: Create new resources
   - PUT: Update resources (replace entirely)
   - PATCH: Partial updates
   - DELETE: Remove resources

3. Statelessness: All requests contain all information needed to process them

4. Status Codes:
   - 200 OK: Successful request
   - 201 Created: Resource successfully created
   - 400 Bad Request: Client error, invalid syntax
   - 401 Unauthorized: Authentication required
   - 403 Forbidden: Client lacks permissions
   - 404 Not Found: Resource doesn't exist
   - 500 Internal Server Error: Server-side errors

5. JSON is the standard format for request/response bodies

6. Clear, consistent endpoints with versioning:
   - /api/v1/users

7. Filtering, sorting, pagination for collections:
   - /api/v1/products?category=electronics&sort=price&page=2

8. HATEOAS (Hypermedia as the Engine of Application State):
   - Responses include links to related resources
"""

# Simple demonstration of both frameworks

if __name__ == "__main__":
    print("Please see the flask_app and fastapi_app directories for working examples.")
    print("This file serves as a reference for comparing Flask and FastAPI.")