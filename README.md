# Mauli Industries ERP System

ERP System for Aerospace and Defense Division

## Features

- **Authentication System**: JWT-based authentication with role-based access control
- **User Management**: Complete user management with super admin capabilities
- **Department Management**: Organizational structure management
- **Security**: Password hashing, JWT tokens, role-based permissions
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **API Documentation**: OpenAPI/Swagger
- **Database Migrations**: Alembic

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd mauli-industries-erp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials and settings
   ```

5. **Set up PostgreSQL database**
   ```sql
   CREATE DATABASE mauli_industries_erp;
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

## Configuration

Edit the `.env` file with your settings:

```env
DATABASE_URL=postgresql://postgres:password@localhost/mauli_industries_erp
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SUPER_ADMIN_EMAIL=admin@mauliindustries.com
SUPER_ADMIN_PASSWORD=admin123
```

## Running the Application

### Development Mode
```bash
python run.py
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## Default Super Admin

The system automatically creates a super admin user on first startup:
- **Username**: admin
- **Email**: (configured in .env)
- **Password**: (configured in .env)

## API Endpoints

### Authentication
- `POST /auth/login` - User login
- `GET /auth/me` - Get current user info

### Users (Super Admin only)
- `POST /users/` - Create user
- `GET /users/` - List users
- `GET /users/{user_id}` - Get user
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

## User Roles

1. **SUPER_ADMIN**: Full system access
2. **ADMIN**: Administrative access
3. **MANAGER**: Department management
4. **EMPLOYEE**: Basic access

## Database Migrations

### Create new migration
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations
```bash
alembic upgrade head
```

### Rollback migration
```bash
alembic downgrade -1
```

## Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- CORS protection
- Input validation with Pydantic

## Development

### Project Structure
```
app/
├── core/           # Configuration and security
├── database/       # Database connection
├── models/         # SQLAlchemy models
├── routers/        # API routes
├── schemas/        # Pydantic schemas
└── main.py         # FastAPI application
```

### Adding New Features

1. Create model in `app/models/`
2. Create Pydantic schemas in `app/schemas/`
3. Create API routes in `app/routers/`
4. Include router in `app/main.py`
5. Generate and apply database migration

## License

© 2024 Mauli Industries - Aerospace and Defense Division
