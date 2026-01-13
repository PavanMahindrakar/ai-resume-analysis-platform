# Testing Guide

This directory contains comprehensive tests for the AI Resume Intelligence backend.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests (isolated component tests)
│   ├── test_auth.py        # Authentication logic tests
│   └── test_matching_engine.py  # Matching engine tests
└── integration/            # Integration tests (API endpoint tests)
    ├── test_auth_api.py    # Authentication API tests
    ├── test_resume_api.py  # Resume upload API tests
    └── test_analysis_api.py # Analysis API tests
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/unit/test_auth.py
pytest tests/integration/test_auth_api.py
```

### Run with coverage
```bash
pytest --cov=app --cov-report=html
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test
```bash
pytest tests/unit/test_auth.py::TestPasswordHashing::test_hash_password_creates_different_hash
```

## Unit Tests vs Integration Tests

### Unit Tests

**What they are:**
- Test individual functions, methods, or components in isolation
- Mock external dependencies (databases, APIs, file systems)
- Fast execution (milliseconds per test)
- Focus on logic correctness

**Example:** Testing `hash_password()` function
- Input: plain text password
- Output: hashed password
- No database, no API calls, just the function

**When to use:**
- Testing business logic
- Testing utility functions
- Testing algorithms (like matching engine)
- Testing data transformations

**Benefits:**
- Fast feedback
- Easy to debug (isolated failures)
- Can test edge cases easily
- Don't require full system setup

### Integration Tests

**What they are:**
- Test multiple components working together
- Use real dependencies (test database, file system)
- Slower execution (seconds per test)
- Focus on component interaction

**Example:** Testing `/api/v1/auth/login` endpoint
- HTTP request → Authentication → Database query → JWT generation → Response
- Tests the entire flow

**When to use:**
- Testing API endpoints
- Testing database operations
- Testing file uploads
- Testing authentication flows

**Benefits:**
- Catch integration bugs
- Test real-world scenarios
- Verify API contracts
- Ensure components work together

## Why Testing Matters for Production Apps

### 1. **Prevent Regressions**
- **Problem:** New feature breaks existing functionality
- **Solution:** Tests catch breaking changes immediately
- **Example:** Changing password hashing algorithm shouldn't break login

### 2. **Documentation**
- Tests serve as executable documentation
- Show how code is supposed to work
- Examples of correct usage
- **Example:** `test_login_success()` shows the login flow

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
- Cheaper to fix bugs early
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

## Test Coverage Goals

- **Critical paths:** 90%+ coverage
  - Authentication
  - Analysis logic
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

1. **Test Naming:** Clear, descriptive names
   - ✅ `test_login_success`
   - ❌ `test1`

2. **Arrange-Act-Assert:** Structure tests clearly
   ```python
   def test_example():
       # Arrange: Set up test data
       user = create_test_user()
       
       # Act: Perform action
       result = login(user.email, user.password)
       
       # Assert: Verify result
       assert result.success is True
   ```

3. **One Assertion Per Test:** Focus on one thing
   - ✅ `test_password_hash_different`
   - ❌ `test_password_hash_and_verify_and_length`

4. **Test Edge Cases:**
   - Empty inputs
   - Null values
   - Boundary conditions
   - Invalid inputs

5. **Keep Tests Fast:**
   - Use in-memory database for tests
   - Mock external services
   - Avoid file I/O when possible

6. **Test Independence:**
   - Each test should run independently
   - Don't rely on test execution order
   - Clean up after tests

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
```

### Testing Business Logic
```python
def test_matching_engine(engine):
    result = engine.analyze(resume_text, job_text)
    assert 0 <= result["match_score"] <= 100
    assert "matched_keywords" in result
```

## Continuous Integration

Tests should run automatically:
- On every commit
- Before merging PRs
- Before deployment

This ensures code quality and prevents broken code from reaching production.
