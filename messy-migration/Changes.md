# CHANGES.md

## Major Issues Identified
- Raw SQL queries with f-strings → vulnerable to SQL injection
- Inconsistent error handling and missing HTTP status codes
- Monolithic file structure
- No tests or input validations

## Fixes & Improvements
- Used parameterized queries to prevent SQL injection
- Validated request data in POST/PUT
- Implemented consistent JSON responses with proper HTTP codes
- Started splitting routes and DB logic (if modularized)
- Added error handling using try-except
- Implemented bcrypt password hashing (in login and signup)

## AI Usage
- Used ChatGPT (OpenAI) to:
  - Help with refactoring endpoints securely
  - Guide project structure improvements
  - Help identify SQL injection risks and fix them

## Assumptions
- All user data is simple (name, email, password)
- Email is unique
- SQLite is used for local testing

## With More Time
- Add unit tests using `pytest` or `unittest`
- Use SQLAlchemy ORM for DB abstraction
- Modularize fully into Flask Blueprints
- Add logging, config file management
