# Backend Setup Guide

Complete guide to set up and run the AI Resume Intelligence backend server.

## Prerequisites

- **Python 3.11+** (check with `python --version`)
- **PostgreSQL 14+** (or SQLite for quick testing)
- **pip** (Python package manager)

## Quick Start (5 Minutes)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Environment File

Create a file named `.env` in the `backend` directory with the following content:

```env
# Database Configuration
# Option 1: SQLite (Quick Testing - No PostgreSQL needed!)
DATABASE_URL=sqlite:///./ai_resume_intelligence.db

# Option 2: PostgreSQL (Uncomment and configure if you have PostgreSQL)
# DATABASE_URL=postgresql://username:password@localhost:5432/ai_resume_intelligence

# JWT Authentication
SECRET_KEY=dev-secret-key-change-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS Configuration (comma-separated list for frontend)
CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]
CORS_CREDENTIALS=True

# Database Pool Settings
DB_ECHO=False
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_PRE_PING=True

# File Storage
UPLOAD_DIR=storage/resumes
```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

This creates all necessary database tables.

### 6. Start the Server

**Option 1: Using Python (Recommended)**
```bash
python main.py
```

**Option 2: Using uvicorn directly**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Verify Server is Running

Open your browser and visit:
- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

You should see the FastAPI interactive documentation.

---

## Database Setup Options

### Option A: SQLite (Quick Testing - Recommended for Development)

**Pros:** No installation needed, works immediately  
**Cons:** Not suitable for production

Just use this in your `.env`:
```env
DATABASE_URL=sqlite:///./ai_resume_intelligence.db
```

No additional setup required!

### Option B: PostgreSQL (Production Ready)

**Pros:** Production-ready, better performance  
**Cons:** Requires PostgreSQL installation

1. **Install PostgreSQL** (if not installed)
   - Windows: Download from https://www.postgresql.org/download/windows/
   - Mac: `brew install postgresql`
   - Linux: `sudo apt-get install postgresql`

2. **Start PostgreSQL Service**
   - Windows: Check Services app
   - Mac/Linux: `pg_ctl start` or `sudo service postgresql start`

3. **Create Database**
   ```sql
   CREATE DATABASE ai_resume_intelligence;
   ```

4. **Update `.env`** with your credentials:
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/ai_resume_intelligence
   ```

---

## Common Issues & Solutions

### Issue: "Module not found" or Import Errors

**Solution:**
1. Ensure virtual environment is activated (you should see `(venv)` in prompt)
2. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Issue: "Database connection failed" or "OperationalError"

**Solution:**
1. **For SQLite:** Ensure the backend directory is writable
2. **For PostgreSQL:**
   - Verify PostgreSQL is running: `pg_isready` (Mac/Linux) or check Services (Windows)
   - Check DATABASE_URL in `.env` matches your PostgreSQL setup
   - Test connection: `psql -U username -d ai_resume_intelligence`

### Issue: "Port 8000 already in use"

**Solution:**
1. Change PORT in `.env` to a different port (e.g., `PORT=8001`)
2. Or stop the process using port 8000:
   - Windows: `netstat -ano | findstr :8000` then `taskkill /PID <pid> /F`
   - Mac/Linux: `lsof -ti:8000 | xargs kill`

### Issue: "Alembic migration errors"

**Solution:**
```bash
# Check current migration status
alembic current

# If database is empty, create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### Issue: "Permission denied" on Windows PowerShell

**Solution:**
If you get "execution of scripts is disabled" when activating venv:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "No module named 'uvicorn'"

**Solution:**
```bash
# Make sure venv is activated, then:
pip install uvicorn[standard]
```

---

## Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | Database connection string | `postgresql://user:password@localhost:5432/ai_resume_intelligence` | Yes |
| `SECRET_KEY` | JWT token signing key | `your-secret-key-change-in-production` | Yes |
| `DEBUG` | Enable debug mode (auto-reload) | `False` | No |
| `HOST` | Server host | `0.0.0.0` | No |
| `PORT` | Server port | `8000` | No |
| `CORS_ORIGINS` | Allowed CORS origins (JSON array) | `["http://localhost:3000","http://localhost:5173"]` | No |
| `CORS_CREDENTIALS` | Allow CORS credentials | `True` | No |
| `UPLOAD_DIR` | Resume storage directory | `storage/resumes` | No |
| `DB_ECHO` | Log SQL queries (debugging) | `False` | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT token expiration | `30` | No |

---

## Running the Server

### Development Mode (Auto-reload on code changes)
```bash
python main.py
# Or
uvicorn app.main:app --reload
```

### Production Mode
```bash
# Install production server
pip install gunicorn

# Run with multiple workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## Testing

Run the test suite to verify everything works:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/integration/test_auth_api.py

# Run with verbose output
pytest -v
```

---

## API Endpoints

Once running, the API is available at `http://localhost:8000/api/v1`

### Key Endpoints:

**Authentication:**
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login user

**Health:**
- `GET /api/v1/health` - Health check endpoint

**Documentation:**
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

### Example: Test Registration

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword123"}'
```

---

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   ├── core/             # Core configuration and dependencies
│   ├── infrastructure/  # Database, AI, storage
│   └── main.py          # FastAPI application
├── alembic.ini          # Alembic configuration
├── main.py              # Server entry point
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (create this)
```

---

## Next Steps

1. ✅ Backend server is running
2. Start the frontend: `cd ../frontend && npm run dev`
3. Test registration: Open http://localhost:5173/register
4. Check API docs: Open http://localhost:8000/docs

---

## Additional Resources

- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **SQLAlchemy Documentation:** https://docs.sqlalchemy.org/
- **Alembic Documentation:** https://alembic.sqlalchemy.org/

---

## Getting Help

If you encounter issues:
1. Check the error message in the terminal
2. Verify all prerequisites are installed
3. Ensure `.env` file is configured correctly
4. Check that the database is accessible
5. Review the Common Issues section above

For database-specific issues, ensure:
- PostgreSQL is running (if using PostgreSQL)
- Database exists and credentials are correct
- Migrations have been run (`alembic upgrade head`)
