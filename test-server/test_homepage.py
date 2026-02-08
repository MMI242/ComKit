import pytest
import requests
import sys

# Base URL untuk API server
try:
    BASE_URL = sys.argv[1]
except IndexError:
    BASE_URL = "http://localhost:8000"

# Test user credentials (user harus sudah ada di server)
TEST_USER = "testuser"
TEST_PASSWORD = "testpassword"


def get_access_token():
    """Helper function untuk login dan mendapatkan access token"""
    print("Login untuk mendapatkan access token...")
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {
        "username": TEST_USER,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(login_url, json=login_payload)
    assert response.status_code == 200, f"Login gagal: {response.text}"
    
    data = response.json()
    access_token = data["access_token"]
    print(f"Access token: {access_token[:20]}...")
    
    return access_token


def test_get_items_success():
    """Test GET /items tanpa parameter (page 1, all types)"""
    access_token = get_access_token()
    
    print("\nTesting GET /items")
    url = f"{BASE_URL}/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200, f"GET /items gagal: {response.text}"
    data = response.json()
    
    print("Cek struktur response")
    assert "items" in data
    assert "pagination" in data
    
    print("Cek pagination structure")
    pagination = data["pagination"]
    assert "current_page" in pagination
    assert "total_pages" in pagination
    assert "total_items" in pagination
    assert "items_per_page" in pagination
    assert pagination["items_per_page"] == 25
    
    print("Cek items structure")
    if len(data["items"]) > 0:
        item = data["items"][0]
        assert "id" in item
        assert "name" in item
        assert "description" in item
        assert "qty" in item
        assert "remaining_qty" in item
        assert "unit" in item
        assert "thumbnail_url" in item
        assert "photo_url" in item
        assert "type" in item
        assert "status" in item
        assert "owner" in item
        
        print("Cek owner structure")
        owner = item["owner"]
        assert "id" in owner
        assert "username" in owner
        assert "name" in owner
        assert "address" in owner
    
    print(f"GET /items sukses: {len(data['items'])} items, page {pagination['current_page']}/{pagination['total_pages']}")


def test_get_items_with_pagination():
    """Test GET /items dengan parameter page"""
    access_token = get_access_token()
    
    print("\nTesting GET /items?page=1")
    url = f"{BASE_URL}/items?page=1"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["pagination"]["current_page"] == 1
    
    print(f"Pagination sukses: page {data['pagination']['current_page']}")


def test_get_items_with_search():
    """Test GET /items dengan parameter search"""
    access_token = get_access_token()
    
    print("\nTesting GET /items?search=test")
    url = f"{BASE_URL}/items?search=test"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    
    print(f"Search sukses: {len(data['items'])} items found")


def test_get_items_with_type_filter():
    """Test GET /items dengan filter type=borrow"""
    access_token = get_access_token()
    
    print("\nTesting GET /items?type=borrow")
    url = f"{BASE_URL}/items?type=borrow"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    print("Validasi semua items bertipe borrow")
    for item in data["items"]:
        assert item["type"] == "borrow", f"Item {item['id']} bukan type borrow"
    
    print(f"Filter type=borrow sukses: {len(data['items'])} items")


def test_get_items_with_type_share():
    """Test GET /items dengan filter type=share"""
    access_token = get_access_token()
    
    print("\nTesting GET /items?type=share")
    url = f"{BASE_URL}/items?type=share"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    print("Validasi semua items bertipe share")
    for item in data["items"]:
        assert item["type"] == "share", f"Item {item['id']} bukan type share"
    
    print(f"Filter type=share sukses: {len(data['items'])} items")


def test_get_items_with_all_parameters():
    """Test GET /items dengan semua parameter"""
    access_token = get_access_token()
    
    print("\nTesting GET /items?page=1&search=test&type=all")
    url = f"{BASE_URL}/items?page=1&search=test&type=all"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "pagination" in data
    
    print("GET /items dengan semua parameter sukses")


def test_get_items_unauthorized():
    """Test GET /items tanpa token"""
    print("\nTesting GET /items tanpa token")
    url = f"{BASE_URL}/items"
    
    response = requests.get(url)
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    
    print("Unauthorized test sukses")


def test_get_items_invalid_token():
    """Test GET /items dengan token invalid"""
    print("\nTesting GET /items dengan token invalid")
    url = f"{BASE_URL}/items"
    headers = {"Authorization": "Bearer invalid_token_string"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 401
    data = response.json()
    assert "error" in data
    
    print("Invalid token test sukses")


def test_get_items_page_out_of_range():
    """Test GET /items dengan page number terlalu besar"""
    access_token = get_access_token()
    
    print("\nTesting GET /items?page=9999")
    url = f"{BASE_URL}/items?page=9999"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 0, "Items harus kosong untuk page out of range"
    
    print("Page out of range test sukses")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
