
# Register sukses
# Username duplicate
# Username terlalu pendek
# Username uppercase
# Username karakter invalid
# Password terlalu pendek
# Missing username
# Missing password
# Missing name
# Missing address
# Field kosong
# Username dengan underscore (valid)

import pytest
import requests
import uuid
import sys

# Base URL untuk API server
try:
    BASE_URL = sys.argv[1]
except IndexError:
    BASE_URL = "http://localhost:8000"


def generate_unique_username():
    """Generate username unik untuk testing"""
    return f"testuser_{uuid.uuid4().hex[:8]}"


def test_register_success():
    """Test register dengan data yang valid"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": generate_unique_username(),
        "password": "testpassword",
        "name": "Test User",
        "address": "Jl. Test No. 123 RT 01",
        "community_id": 1
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 201
    data = response.json()
    
    # Cek struktur response (auto login)
    assert "access_token" in data
    assert "refresh_token" in data
    assert "token_type" in data
    assert "expires_in" in data
    assert "user" in data
    
    # Cek token type
    assert data["token_type"] == "Bearer"
    
    # Cek user data
    user = data["user"]
    assert "id" in user
    assert "username" in user
    assert "name" in user
    assert "address" in user
    assert user["username"] == payload["username"]
    assert user["name"] == payload["name"]
    assert user["address"] == payload["address"]


def test_register_duplicate_username():
    """Test register dengan username yang sudah ada"""
    url = f"{BASE_URL}/auth/register"
    
    # Register pertama kali
    username = generate_unique_username()
    payload = {
        "username": username,
        "password": "testpassword",
        "name": "Test User",
        "address": "Jl. Test No. 123"
    }
    response1 = requests.post(url, json=payload)
    assert response1.status_code == 201
    
    # Register dengan username yang sama
    response2 = requests.post(url, json=payload)
    
    assert response2.status_code == 409
    data = response2.json()
    assert "error" in data
    assert "already exists" in data["error"].lower()


def test_register_username_too_short():
    """Test register dengan username kurang dari 3 karakter"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": "ab",
        "password": "testpassword",
        "name": "Test User",
        "address": "Jl. Test No. 123"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_register_username_uppercase():
    """Test register dengan username mengandung huruf besar"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": "TestUser123",
        "password": "testpassword",
        "name": "Test User",
        "address": "Jl. Test No. 123"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "lowercase" in data["error"].lower()


def test_register_username_invalid_chars():
    """Test register dengan username mengandung karakter tidak valid"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": "test-user@123",
        "password": "testpassword",
        "name": "Test User",
        "address": "Jl. Test No. 123"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data


def test_register_password_too_short():
    """Test register dengan password kurang dari 6 karakter"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": generate_unique_username(),
        "password": "12345",
        "name": "Test User",
        "address": "Jl. Test No. 123"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "password" in data["error"].lower()


def test_register_missing_username():
    """Test register tanpa username"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "password": "testpassword",
        "name": "Test User",
        "address": "Jl. Test No. 123"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 422]


def test_register_missing_password():
    """Test register tanpa password"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": generate_unique_username(),
        "name": "Test User",
        "address": "Jl. Test No. 123"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 422]


def test_register_missing_name():
    """Test register tanpa name"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": generate_unique_username(),
        "password": "testpassword",
        "address": "Jl. Test No. 123"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 422]


def test_register_missing_address():
    """Test register tanpa address"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": generate_unique_username(),
        "password": "testpassword",
        "name": "Test User"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 422]


def test_register_empty_fields():
    """Test register dengan field kosong"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": "",
        "password": "",
        "name": "",
        "address": ""
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 422]


def test_register_with_underscore():
    """Test register dengan username mengandung underscore (valid)"""
    url = f"{BASE_URL}/auth/register"
    payload = {
        "username": f"test_user_{uuid.uuid4().hex[:6]}",
        "password": "testpassword",
        "name": "Test User",
        "address": "Jl. Test No. 123"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 201


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
