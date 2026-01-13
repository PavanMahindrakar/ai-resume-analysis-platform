# Testing Guide

## Overview

This project uses **pytest** for testing. Tests are organized into:
- **Unit tests**: Test individual functions/components in isolation
- **Integration tests**: Test API endpoints and component interactions

## Quick Start

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest
```

### Run Specific Test Categories
```bash
# Unit tests only
pytest tests/unit/

# Integration tests only
pytest tests/integration/

# Specific test file
pytest tests/unit/test_auth.py
```

### Run with Coverage
```bash
pytest --cov=app --cov-report=html
# Open htmlcov/index.html to view coverage report
```

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures (database, test client, etc.)
├── unit/                    # Unit tests
│   ├── test_auth.py        # Authentication logic (hashing, JWT)
│   └── test_matching_engine.py  # Matching engine algorithms
└── integration/            # Integration tests
    ├── test_auth_api.py    # Authentication API endpoints
    ├── test_resume_api.py  # Resume upload API endpoints
    └── test_analysis_api.py # Analysis API endpoints
```

## Unit Tests vs Integration Tests

### Unit Tests

**Definition:**
Unit tests verify individual functions, methods, or components work correctly **in isolation**. They mock external dependencies (databases, APIs, file systems).

**Characteristics:**
- ✅ Fast execution (milliseconds)
- ✅ Isolated (no external dependencies)
- ✅ Easy to debug
- ✅ Test edge cases easily

**Example:**
```python
def test_hash_password_creates_different_hash():
    """Test that hashing creates different hashes (due to salt)."""
    password = "testpassword123"
    hash1 = hash_password(password)
    hash2 = hash_password(password)
    
    # Hashes should be different (bcrypt uses random salt)
    assert hash1 != hash2
    # But both should verify correctly
    assert verify_password(password, hash1)
    assert verify_password(password, hash2)
```

**When to Use:**
- Testing business logic (matching engine, calculations)
- Testing utility functions (password hashing, text processing)
- Testing algorithms (keyword extraction, scoring)
- Testing data transformations

**Benefits:**
- Fast feedback during development
- Pinpoint exact failure location
- Can test many edge cases quickly
- Don't require database or API setup

### Integration Tests

**Definition:**
Integration tests verify multiple components work together correctly. They use real dependencies (test database, file system).

**Characteristics:**
- ⏱️ Slower execution (seconds)
- 🔗 Test component interactions
- 🌐 Use real dependencies
- 🎯 Test end-to-end flows

**Example:**
```python
def test_login_success(client, test_user):
    """Test successful login endpoint."""
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "test@example.com",
            "password": "testpassword123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
```

**When to Use:**
- Testing API endpoints
- Testing database operations
- Testing file uploads
- Testing authentication flows
- Testing component integration

**Benefits:**
- Catch integration bugs
- Test real-world scenarios
- Verify API contracts
- Ensure components work together

## Why Testing Matters for Production Apps

### 1. **Prevent Regressions**
**Problem:** New feature breaks existing functionality  
**Solution:** Tests catch breaking changes immediately  
**Example:** Changing password hashing algorithm shouldn't break login

### 2. **Documentation**
Tests serve as **executable documentation**:
- Show how code is supposed to work
- Provide examples of correct usage
- Document expected behavior
- **Example:** `test_login_success()` shows the complete login flow

### 3. **Confidence in Refactoring**
- Can safely improve code structure
- Tests verify behavior hasn't changed
- **Example:** Refactoring matching engine without breaking analysis

### 4. **Faster Debugging**
- Tests pinpoint where bugs occur
- Isolated tests = isolated failures
- **Example:** Test fails → know exactly which function is broken

### 5. **Catch Bugs Early**
- Find issues during development, not production
- Cheaper to fix bugs early (10x cost difference)
- **Example:** Test catches edge case before user reports it

### 6. **Team Collaboration**
- Tests ensure code works as expected
- New developers can verify their changes
- **Example:** PR reviewer runs tests to verify changes

### 7. **Production Stability**
- More tests = fewer production bugs
- Critical paths are tested
- **Example:** Authentication is thoroughly tested

### 8. **Performance Monitoring**
- Tests can catch performance regressions
- **Example:** Matching engine should complete in < 1 second

### 9. **Compliance & Security**
- Tests verify security measures work
- **Example:** Password hashing, JWT validation, authorization

### 10. **Continuous Integration**
- Automated testing in CI/CD pipeline
- Prevents broken code from reaching production
- **Example:** Tests run on every commit

## Test Coverage Goals

- **Critical paths:** 90%+ coverage
  - Authentication (password hashing, JWT)
  - Analysis logic (matching engine)
  - Security functions

- **API endpoints:** 80%+ coverage
  - All success cases
  - All error cases
  - Edge cases

- **Business logic:** 85%+ coverage
  - Matching engine
  - Keyword extraction
  - Score calculation

## Best Practices

### 1. Test Naming
Use clear, descriptive names:
- ✅ `test_login_success`
- ✅ `test_hash_password_creates_different_hash`
- ❌ `test1`
- ❌ `test_auth`

### 2. Arrange-Act-Assert Pattern
Structure tests clearly:
```python
def test_example():
    # Arrange: Set up test data
    user = create_test_user()
    
    # Act: Perform action
    result = login(user.email, user.password)
    
    # Assert: Verify result
    assert result.success is True
```

### 3. One Assertion Per Test (when possible)
Focus on one thing:
- ✅ `test_password_hash_different`
- ✅ `test_password_verify_correct`
- ❌ `test_password_hash_and_verify_and_length`

### 4. Test Edge Cases
- Empty inputs
- Null values
- Boundary conditions
- Invalid inputs
- **Example:** `test_extract_keywords_empty()`

### 5. Keep Tests Fast
- Use in-memory database for tests
- Mock external services
- Avoid file I/O when possible
- **Example:** SQLite in-memory database

### 6. Test Independence
- Each test should run independently
- Don't rely on test execution order
- Clean up after tests
- **Example:** Each test gets fresh database session

### 7. Use Fixtures
Share common setup:
```python
@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(email="test@example.com", ...)
    db_session.add(user)
    db_session.commit()
    return user
```

## Common Test Patterns

### Testing Authentication
```python
def test_login_success(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "correct_password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Testing Error Cases
```python
def test_login_wrong_password(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": test_user.email,
        "password": "wrong_password"
    })
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()
```

### Testing Business Logic
```python
def test_matching_engine(engine):
    result = engine.analyze(resume_text, job_text)
    assert 0 <= result["match_score"] <= 100
    assert "matched_keywords" in result
```

### Testing File Uploads
```python
def test_upload_pdf_success(authenticated_client):
    pdf_content = b"%PDF-1.4\n..."
    response = authenticated_client.post(
        "/api/v1/resume/upload",
        files={"file": ("resume.pdf", pdf_content, "application/pdf")}
    )
    assert response.status_code == 201
```

## Running Tests in CI/CD

Tests should run automatically:
- On every commit
- Before merging PRs
- Before deployment

Example GitHub Actions:
```yaml
- name: Run tests
  run: |
    cd backend
    pytest --cov=app --cov-report=xml
```

## Debugging Failed Tests

### Verbose Output
```bash
pytest -v -s  # -s shows print statements
```

### Run Specific Test
```bash
pytest tests/unit/test_auth.py::TestPasswordHashing::test_hash_password_creates_different_hash
```

### Show Local Variables
```bash
pytest --tb=long  # Shows more context
```

### Use Debugger
```python
def test_example():
    import pdb; pdb.set_trace()  # Breakpoint
    # ... test code
```

## Summary

**Unit Tests:**
- Fast, isolated, test individual functions
- Use for: business logic, utilities, algorithms

**Integration Tests:**
- Slower, test component interactions
- Use for: API endpoints, database operations, file uploads

**Why Testing Matters:**
- Prevents regressions
- Documents code behavior
- Enables safe refactoring
- Catches bugs early
- Improves production stability
- Enables CI/CD automation
