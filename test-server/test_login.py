import pytest
import requests
import sys

# Base URL untuk API server
try:
    BASE_URL = sys.argv[1]
except IndexError:
    BASE_URL = "http://localhost:8000"

# user sudah ada di server
TEST_USER = "testuser"
TEST_PASSWORD = "testpassword"


def test_login_success():
    """Test login dengan kredensial yang valid"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Cek struktur response
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
    assert "community_id" in user
    assert user["username"] == "testuser"


def test_login_invalid_username():
    """Test login dengan username yang tidak ada"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": "usertiada",
        "password": "testpassword"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data


def test_login_invalid_password():
    """Test login dengan password yang salah"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data


def test_login_missing_username():
    """Test login tanpa username"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "password": "testpassword"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 422]  # Bad request atau validation error


def test_login_missing_password():
    """Test login tanpa password"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": "testuser"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 422]


def test_login_empty_credentials():
    """Test login dengan kredensial kosong"""
    url = f"{BASE_URL}/auth/login"
    payload = {
        "username": "",
        "password": ""
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 401, 422]


def test_refresh_token_success():
    """Test refresh token dengan refresh token yang valid"""
    # Login dulu untuk dapat refresh token
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {
        "username": "testuser",
        "password": "testpassword"
    }
    login_response = requests.post(login_url, json=login_payload)
    assert login_response.status_code == 200
    
    refresh_token = login_response.json()["refresh_token"]
    
    # Test refresh token
    refresh_url = f"{BASE_URL}/auth/refresh"
    refresh_payload = {
        "refresh_token": refresh_token
    }
    
    response = requests.post(refresh_url, json=refresh_payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Cek struktur response
    assert "access_token" in data
    assert "token_type" in data
    assert "expires_in" in data
    assert data["token_type"] == "Bearer"


def test_refresh_token_invalid():
    """Test refresh token dengan token yang tidak valid"""
    url = f"{BASE_URL}/auth/refresh"
    payload = {
        "refresh_token": "invalid_token_string"
    }
    
    response = requests.post(url, json=payload)
    
    assert response.status_code == 401


def test_refresh_token_missing():
    """Test refresh token tanpa mengirim token"""
    url = f"{BASE_URL}/auth/refresh"
    payload = {}
    
    response = requests.post(url, json=payload)
    
    assert response.status_code in [400, 422]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
