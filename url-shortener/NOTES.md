# URL Shortener Service Documentation

## Overview

This URL Shortener Service is a lightweight and efficient web API built using Python and Flask. It enables users to shorten long URLs into concise 6-character alphanumeric codes, redirect users from the shortened URLs to their original destinations, and retrieve analytics data about usage. The system stores all data in-memory, making it simple and fast, suitable for learning and demonstration environments.

## Project Structure

```
url-shortener/
├── app/
│   ├── __init__.py       # Empty initializer for the package
│   ├── main.py           # Flask application: API endpoints and server setup
│   ├── models.py         # URL storage and management with thread-safe operations
│   ├── utils.py          # Utility functions for URL validation and short code generation
├── tests/
│   └── test_basic.py     # Basic tests validating core API endpoints
├── .gitignore            # Ignored files and folders
├── requirements.txt      # Python package dependencies
```

## Features

- **Shorten URLs:**  
  Accepts a JSON POST request with a long URL, validates it, and returns a short 6-character alphanumeric code alongside the fully qualified shortened URL.

- **Redirect:**  
  Accessing the shortened URL (`GET /`) redirects (HTTP 302) users to the original long URL. Each access increments the click count.

- **Analytics:**  
  Provides statistics for each short code via `GET /api/stats/`, returning the original URL, total clicks, and creation time.

- **Health Checks:**  
  Endpoints (`/` and `/api/health`) to verify service status.

- **Thread Safety:**  
  Uses Python threading locks to safely handle concurrent requests and state modifications.

- **In-memory Data Storage:**  
  Keeps URL mappings and metadata in RAM without external databases.

## Getting Started

### Prerequisites

- Python 3.8 or newer

### Installation

1. Clone or download the repository.
2. Navigate to the project directory.
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the Flask development server:

   ```bash
   python -m flask --app app.main run
   ```

   The API will be available at: `http://localhost:5000`

### Running Tests

Use `pytest` to run the test suite:

```bash
pytest
```

## API Endpoints

### 1. Health Checks

- **GET /**  
  Returns basic service health info:

  ```json
  {
    "status": "healthy",
    "service": "URL Shortener API"
  }
  ```

- **GET /api/health**  
  Returns API-specific health status:

  ```json
  {
    "status": "ok",
    "message": "URL Shortener API is running"
  }
  ```

### 2. Shorten URL

- **POST /api/shorten**  
  Request Body (JSON):

  ```json
  {
    "url": "https://www.example.com/very/long/url"
  }
  ```

- **Success Response:**

  - StatusCode: `201 Created`

  ```json
  {
    "short_code": "abc123",
    "short_url": "http://localhost:5000/abc123"
  }
  ```

- **Error Responses:**

  - `400 Bad Request` if URL is missing or invalid:

    ```json
    {
      "error": "Invalid URL"
    }
    ```

  - `500 Internal Server Error` if unable to generate a unique short code.

### 3. Redirect to Original URL

- **GET /**

- **Behavior:**
  - Redirects (HTTP 302) to the original URL.
  - Increments internal click count for analytics.
  - Returns `404 Not Found` if the code does not exist.

### 4. View URL Analytics

- **GET /api/stats/**

- **Success Response:**

  ```json
  {
    "url": "https://www.example.com/very/long/url",
    "clicks": 10,
    "created_at": "2024-01-01T10:00:00"
  }
  ```

- **Error Response:**

  - `404 Not Found` if short code does not exist:

    ```json
    {
      "error": "Short code not found"
    }
    ```

## Implementation Details

### URLStore (models.py)

- Manages in-memory storage of URL mappings.
- Uses a `threading.Lock` to ensure thread-safe access and modifications.
- Stores the original URL, creation timestamp (ISO 8601 UTC), and cumulative clicks per short code.
- Provides methods to `add`, `get`, and `increment_clicks`.

### Utility Functions (utils.py)

- `generate_short_code(length=6)`:  
  Produces a random alphanumeric string of the specified length to serve as a unique key for shortened URLs.

- `is_valid_url(url)`:  
  Performs basic regex-based validation to verify the URL starts with `http://` or `https://` and follows a conventional domain/path format.

### Flask Application (main.py)

- Defines API routes corresponding to core service features plus health checks.
- Uses the `URLStore` singleton instance to manage URLs.
- Implements validation and error handling to communicate issues clearly with appropriate HTTP status codes.
- Ensures uniqueness of short codes, retrying up to 10 times if conflicts occur.

### Thread Safety

- The service supports concurrent requests safely within its Flask dev server context by locking shared data access.

### Testing (test_basic.py)

- Provides basic unit tests using `pytest` and Flask test client to verify health check endpoints.
- Further testing can and should be added for all major APIs and error scenarios.

## Usage Examples

**Shorten a URL:**
```bash
curl -X POST http://localhost:5000/api/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com/long/url"}'
```

**Follow Short URL (Redirect):**
```bash
curl -L http://localhost:5000/abc123
```

**Get Analytics:**
```bash
curl http://localhost:5000/api/stats/abc123
```

## Notes and Considerations

- This implementation uses in-memory storage, so all data will be lost if the app restarts.
- The short code generation is random and checks uniqueness by retrying; this is efficient for small datasets but might need better strategies for production scale.
- URL validation is basic — more robust parsing could be added as needed.
- No persistence or external database is used per assignment requirements.
- The service does not provide user authentication or web UI.
- Concurrency support is minimal but sufficient for demonstration purposes.
