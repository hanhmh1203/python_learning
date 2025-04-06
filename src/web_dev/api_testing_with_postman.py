"""
API Testing with Postman

This guide demonstrates how to test REST APIs using Postman, focusing on the Flask and FastAPI
applications we've built.
"""

# ===============================
# INTRODUCTION TO POSTMAN
# ===============================

"""
Postman is a popular API client that makes it easy to create, share, test and document APIs.
It offers a simple GUI for sending HTTP requests and viewing responses.

Key features:
- Send requests with different HTTP methods (GET, POST, PUT, DELETE)
- Add request parameters, headers, and body content
- Organize requests into collections
- Create test scripts to validate responses
- Set up environments with variables
"""

# ===============================
# SETTING UP POSTMAN FOR API TESTING
# ===============================

"""
1. Download and install Postman from https://www.postman.com/downloads/
2. Create a new Collection named "User Management API"
3. Set up environment variables (optional):
   - BASE_URL: http://127.0.0.1:5000 (for Flask) or http://127.0.0.1:8000 (for FastAPI)

Testing Steps for our User Management API:
"""

# ===============================
# TESTING FLASK/FASTAPI CRUD OPERATIONS
# ===============================

"""
1. CREATE A USER (POST Request)
   - Endpoint: {{BASE_URL}}/api/users
   - Headers: Content-Type: application/json
   - Body (raw JSON):
     {
       "username": "johndoe",
       "email": "john@example.com",
       "age": 30
     }
   - Expected Response: 201 Created with user ID
   - Test: Verify status code is 201 and response contains user_id

2. GET ALL USERS (GET Request)
   - Endpoint: {{BASE_URL}}/api/users
   - Expected Response: 200 OK with array of users
   - Test: Verify status code is 200 and response contains an array

3. GET SPECIFIC USER (GET Request)
   - Endpoint: {{BASE_URL}}/api/users/1 (use ID from create response)
   - Expected Response: 200 OK with user details
   - Test: Verify status code is 200 and username matches

4. UPDATE USER (PUT Request)
   - Endpoint: {{BASE_URL}}/api/users/1
   - Headers: Content-Type: application/json
   - Body (raw JSON):
     {
       "email": "john.updated@example.com",
       "age": 31
     }
   - Expected Response: 200 OK with updated user
   - Test: Verify status code is 200 and email was updated

5. DELETE USER (DELETE Request)
   - Endpoint: {{BASE_URL}}/api/users/1
   - Expected Response: 204 No Content (FastAPI) or 200 OK (Flask)
   - Test: Verify appropriate status code

6. VERIFY DELETION (GET Request)
   - Endpoint: {{BASE_URL}}/api/users/1
   - Expected Response: 404 Not Found
   - Test: Verify status code is 404
"""

# ===============================
# ADVANCED POSTMAN TESTING FEATURES
# ===============================

"""
1. Automated Test Scripts
   - Add JavaScript tests to verify responses
   - Example test for user creation:
   
   pm.test("Status code is 201", function() {
       pm.response.to.have.status(201);
   });
   
   pm.test("Response contains user ID", function() {
       var jsonData = pm.response.json();
       pm.expect(jsonData.user_id).to.exist;
       // Store ID for later tests
       pm.environment.set("user_id", jsonData.user_id);
   });

2. Collection Runner
   - Run a sequence of requests in order
   - Useful for testing the complete CRUD flow
   - Can pass data between requests using environment variables

3. Environments
   - Create different environments (dev, test, prod)
   - Switch between them easily
   - Store different base URLs and credentials

4. Authentication
   - Basic Auth, API Keys, OAuth 2.0
   - Store tokens for authenticated requests
"""

# ===============================
# DIFFERENCES BETWEEN FLASK AND FASTAPI IN TESTING
# ===============================

"""
When testing the two frameworks, you'll notice some differences:

1. Response Format
   - Flask: We manually structured our responses
   - FastAPI: Responses are automatically validated against Pydantic models

2. Error Handling
   - Flask: Custom error responses with status codes
   - FastAPI: Standardized error format with detailed validation errors

3. Documentation
   - Flask: No built-in API docs (would need Swagger UI manually)
   - FastAPI: Interactive docs at /docs or /redoc
     - You can explore and test the API directly in the browser
     - All parameters, request bodies, and responses are documented

4. Validation
   - Flask: Manual validation in route handlers
   - FastAPI: Automatic validation based on type hints and Pydantic models
     - More detailed validation errors
     - Data conversion handled automatically
"""

# Example Postman test script for both APIs
example_test_script = """
// Test for successful creation
pm.test("Status code is 201", function() {
    pm.response.to.have.status(201);
});

// Store the user ID for subsequent requests
if (pm.response.code === 201) {
    var jsonData = pm.response.json();
    // Different response format between Flask and FastAPI
    if (jsonData.user_id) {
        // Flask response format
        pm.environment.set("user_id", jsonData.user_id);
    } else if (jsonData.id) {
        // FastAPI response format
        pm.environment.set("user_id", jsonData.id);
    }
}

// Verify the username
pm.test("Username is correct", function() {
    var jsonData = pm.response.json();
    // Check in different response formats
    var username = jsonData.username || jsonData.user.username;
    pm.expect(username).to.equal("johndoe");
});
"""

# Main entry point - This is just documentation, not an executable script
if __name__ == "__main__":
    print("This file contains documentation for API testing with Postman.")
    print("It is not meant to be executed as a Python script.")
    print("Please refer to the document comments for step-by-step instructions on API testing.")