# Productivity API

A backend service built with FastAPI that implements a task manager. A budget tracker is planned for future release.
The project focuses on building a production-style API with authentication, database integration, and clean architecture.

## Features

- Task manager CRUD (Postgres-backed)
- User registration and login
- JWT-based authentication
- Protected routes using token validation
- User-scoped task authorization (multi-user support)

## API Overview

Main endpoints:

- POST /auth/register
- POST /auth/login
- GET /tasks
- POST /tasks
- PATCH /tasks/{id}
- DELETE /tasks/{id}

## Tech Stack

- Python 3.13
- FastAPI
- Uvicorn
- PostgreSQL
- SQLAlchemy
- JWT (python-jose)

## Status

Core backend functionality is complete:

- Database integration (Postgres)
- Task CRUD operations
- JWT authentication and authorization

## Roadmap

- Alembic migrations
- Budget tracking module
- Basic frontend for visualization
- Testing (pytest)

## Notes

This project is being built as a backend-focused portfolio piece, emphasizing:
- clean API design
- authentication and authorization
- real-world backend patterns
