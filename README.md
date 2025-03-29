```markdown
# Lucid Task Submission API

A FastAPI-based web application implementing user authentication and post management with JWT, following MVC and DDD principles.

## Features

- JWT Authentication (Signup/Login)
- Post CRUD Operations
- Payload Validation (1MB limit for posts)
- In-Memory Caching (5 minutes TTL)
- Async Database Operations
- Dependency Injection with Punq
- SQLAlchemy ORM with MySQL
- Pydantic Schema Validation

## Installation

### Prerequisites
- Python 3.12
- MySQL database
- Poetry (version 1.4+)

1. Clone repository:
```bash
git clone https://github.com/Mechislav1989/lucid-t.git
cd lucid-t
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
poetry install
```

4. Create `.env` file:
```ini
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_HOST='localhost'
DB_PORT='3306'
DB_NAME='name'
DB_USER='user'
DB_PASS='pass'
```

Or manually:
```bash
docker compose -f docker_compose/app.yaml --env-file .env up --build -d
```

## Running the Server
```bash
uvicorn api.main.create_app --host 0.0.0.0 --port 8000 --reload
```
API will be available at `http://localhost:8000`

## API Documentation
- Swagger UI: `/docs`

## Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /signup  | User registration |
| POST   | /login   | Get JWT token |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   | /posts   | Create new post |
| GET    | /posts   | Get all user posts |
| DELETE | /posts/{id} | Delete post |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /users/me | Get current user info |

## Testing
Use included endpoints with:
- Curl/HTTPie
- Postman
- Swagger UI

Example flow:
1. Signup with email/password
2. Login to get JWT token
3. Use token in Authorization header:
   ```
   Authorization: Bearer <your-token>
   ```
4. Create/Read/Delete posts

## Project Structure
```
project/
├── api/
│   ├── endpoints.py      # Routes
│   └── schemas.py        # Pydantic models
├── application/          # Use Cases
│   ├── posts/
│   └── users/
├── domain/               # Core logic
│   ├── posts/
│   └── users/
├── infrastructure/       # Implementations
│   ├── database.py
│   ├── repositories/
│   └── caching.py
└── requirements.txt
```

## Dependencies
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Passlib
- Python-JOSE
- cachetools
- punq
- asyncpg

## Contributing
1. Fork repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## License
MIT License

---

**Note**: Replace placeholder values in `.env` with your actual database credentials and secret key. Ensure PostgreSQL is running before starting the server.
```
