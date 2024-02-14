### Movie Collection Management API

overview:
  title: "Movie Collection Management API"
  description: "The Movie Collection Management API enables users to manage their movie collections efficiently. Users can perform operations like creating, updating, and deleting collections, as well as retrieving collections with associated movies and top 3 favorite genres."

API Endpoints:
  - title: "User Registration"
    method: "POST"
    url: "http://localhost:8000/register/"
    description: "Allows users to register with a username and password."
    body: "{\"username\": \"<username>\", \"password\": \"<password>\"}"
    response: "Returns JWT tokens upon successful registration."

  - title: "User Login"
    method: "POST"
    url: "http://localhost:8000/login/"
    description: "Allows registered users to log in."
    body: "{\"username\": \"<username>\", \"password\": \"<password>\"}"
    response: "Returns JWT tokens upon successful login."

  - title: "Create Collection"
    method: "POST"
    url: "http://localhost:8000/collection/"
    description: "Allows authenticated users to create a new collection."
    headers: "{\"Authorization\": \"Bearer <access_token>\"}"
    body: "Include collection data (title, description, movies)."
    response: "Returns the UUID of the created collection."

  - title: "Retrieve Collections with Top 3 Favorite Genres"
    method: "GET"
    url: "http://localhost:8000/collection/"
    description: "Allows authenticated users to retrieve their collections with top 3 favorite genres."
    headers: "{\"Authorization\": \"Bearer <access_token>\"}"
    response: "Returns collections with top 3 favorite genres."

  - title: "Update Collection"
    method: "PUT"
    url: "http://localhost:8000/collection/<collection_uuid>/"
    description: "Allows authenticated users to update an existing collection."
    headers: "{\"Authorization\": \"Bearer <access_token>\"}"
    body: "Include updated collection data (title, description, movies)."
    response: "Confirms the update."

  - title: "Delete Collection"
    method: "DELETE"
    url: "http://localhost:8000/collection/<collection_uuid>/"
    description: "Allows authenticated users to delete an existing collection."
    headers: "{\"Authorization\": \"Bearer <access_token>\"}"
    response: "Confirms the deletion."

  - title: "Request Count APIs"
    sub_endpoints:
      - title: "GET request-count"
        method: "GET"
        url: "http://localhost:8000/request-count/"
        description: "Returns the number of requests served by the server till now."
        response: "{\"requests\": <number of requests served by this server till now>}"

      - title: "POST request-count/reset"
        method: "POST"
        url: "http://localhost:8000/request-count/reset/"
        description: "Resets the request count."
        response: "{\"message\": \"Request count reset successfully\"}"

Testing Instructions: >
  1. Register a new user using the User Registration API.
  2. Log in with the registered user credentials using the User Login API.
  3. Create a collection using the Create Collection API.
  4. Retrieve collections with top 3 favorite genres using the Retrieve Collections API.
  5. Update an existing collection using the Update Collection API.
  6. Delete an existing collection using the Delete Collection API.
  7. Use the provided Request Count APIs to monitor and reset the request count.

Ensure to include the appropriate request data and JWT tokens in the headers for authenticated endpoints.
