import pytest
from fastapi.testclient import TestClient
import jwt
import sys
import os
import datetime

# Add the app directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from services.auth import SECRET_KEY, ALGORITHM

client = TestClient(app)

def create_test_token(email: str, expires_delta: datetime.timedelta = None):
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def test_unauthorized_access():
    # Test that accessing a protected route without a token returns 401
    response = client.get("/api/portfolio/summary")
    assert response.status_code == 401

def test_invalid_token():
    # Test that accessing with an invalid token returns 401
    response = client.get(
        "/api/portfolio/summary",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_expired_token():
    # Test that accessing with an expired token returns 401
    token = create_test_token("demo@aurora.ai", expires_delta=datetime.timedelta(minutes=-15))
    response = client.get(
        "/api/portfolio/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_authorized_access():
    # Test that accessing with a valid token works
    token = create_test_token("demo@aurora.ai")
    response = client.get(
        "/api/portfolio/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    # It might fail with 404 if no portfolio is found, but that still means it passed auth
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        assert "name" in response.json()

def test_user_not_found():
    # Test token for non-existent user
    token = create_test_token("nonexistent@example.com")
    response = client.get(
        "/api/portfolio/summary",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "User not found"
