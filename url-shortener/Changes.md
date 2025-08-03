# CHANGES.md

## Project: URL Shortener

### Overview
This project implements a basic URL shortening service similar to Bit.ly or TinyURL, using Python and Flask. It supports three core endpoints:

1. **POST /api/shorten** - to generate a 6-character short code for a given URL.
2. **GET /<short_code>** - to redirect the user to the original long URL.
3. **GET /api/stats/<short_code>** - to fetch analytics data like click count, creation timestamp, and the original URL.

All data is stored in-memory using thread-safe structures. Input validation and error handling have been implemented.

---

## Features Implemented

### ✅ Core Requirements
- [x] URL shortening (`POST /api/shorten`)
- [x] URL redirection (`GET /<short_code>`)
- [x] Analytics (`GET /api/stats/<short_code>`)
- [x] 6-character alphanumeric short codes
- [x] URL validation
- [x] Thread-safe in-memory data storage
- [x] Basic error handling
- [x] 5+ tests using `pytest`

---

## Architecture

- **`app/main.py`**: Main Flask app with all route handlers
- **`app/utils.py`**: Utility functions for short code generation, URL validation
- **`app/storage.py`**: In-memory store for mapping URLs, managing clicks, and timestamps
- **`tests/`**: Test cases for all endpoints and error scenarios

---

## Design Decisions

- Used `threading.Lock` to make access to in-memory store thread-safe
- Used Python `uuid4` + base62 encoding to ensure unique short codes
- Used `datetime.utcnow()` for timestamp consistency
- Used a dictionary for storage with keys as short codes and values as dicts containing:
  ```python
  {
      "original_url": str,
      "clicks": int,
      "created_at": datetime
  }
  ```

---

## Error Handling

- Invalid or missing JSON payload returns `400 Bad Request`
- Invalid or missing URL field returns `422 Unprocessable Entity`
- Non-existent short codes return `404 Not Found`

---

## Tests

- `test_shorten_url_success`: Valid URL shortening
- `test_redirect_valid_code`: Redirects successfully
- `test_redirect_invalid_code`: Returns 404 for unknown code
- `test_stats_valid_code`: Returns stats for existing short code
- `test_stats_invalid_code`: Returns 404 for unknown code
- `test_invalid_url`: Returns error on invalid URL input
- All tests run via `pytest` and pass.

---

## AI Usage

This project used **ChatGPT (GPT-4)** to:

- Plan the initial project structure
- Draft initial route handler code (later reviewed and customized)
- Generate examples of URL validation logic
- Create base test cases using `pytest`
- Draft this `CHANGES.md` file

Manual review, debugging, and enhancements were performed to ensure correctness, thread safety, and clean design. Some AI-generated suggestions were modified or replaced entirely based on practical testing and edge-case handling.

---

## Known Limitations

- Data is lost on app restart (in-memory store only)
- No custom short codes supported
- No rate limiting or usage limits
- No persistent storage (per assignment constraints)

---

## Setup and Run Instructions

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python -m flask --app app.main run

# Run tests
pytest
```

---

## Final Notes

This implementation adheres to all assignment requirements with a focus on simplicity, correctness, and clarity. Code is modular and easy to extend if needed.

