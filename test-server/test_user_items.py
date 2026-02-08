# test CRUD user items

import pytest
import requests
import uuid
import sys

# Base URL untuk API server
try:
    BASE_URL = sys.argv[1]
except IndexError:
    BASE_URL = "http://localhost:8000"


def get_access_token():
    """Helper untuk register user baru dan dapatkan access token"""
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    register_url = f"{BASE_URL}/auth/register"
    register_payload = {
        "username": username,
        "password": "testpassword",
        "name": "Test User",
        "address": "Jl. Test No. 123",
        "community_id": 1
    }
    response = requests.post(register_url, json=register_payload)
    assert response.status_code == 201
    return response.json()["access_token"], username


def test_get_user_items_empty():
    """Test GET /user/items saat belum ada item"""
    access_token, username = get_access_token()
    
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(items_url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0
    print(f"User {username} has 0 items (empty)")


def test_create_user_item_success():
    """Test POST /user/items berhasil"""
    access_token, username = get_access_token()
    
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    item_payload = {
        "name": "Panci Besar",
        "description": "Panci besar 5 liter",
        "qty": 2,
        "unit": "pcs",
        "type": "borrow",
        "status": "available"
    }
    
    response = requests.post(items_url, json=item_payload, headers=headers)
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Panci Besar"
    assert data["qty"] == 2
    assert data["remaining_qty"] == 2
    assert data["unit"] == "pcs"
    assert data["type"] == "borrow"
    assert data["status"] == "available"
    assert "id" in data
    assert "thumbnail_url" in data
    assert "photo_url" in data
    print(f"Item created: {data['id']} - {data['name']}")


def test_create_user_item_missing_fields():
    """Test POST /user/items dengan field kosong"""
    access_token, username = get_access_token()
    
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    item_payload = {
        "name": "Panci"
    }
    
    response = requests.post(items_url, json=item_payload, headers=headers)
    
    assert response.status_code == 400
    assert "error" in response.json()
    print(f"Missing fields rejected: {response.json()['error']}")


def test_create_user_item_invalid_qty():
    """Test POST /user/items dengan qty invalid"""
    access_token, username = get_access_token()
    
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    item_payload = {
        "name": "Panci Besar",
        "description": "Panci besar 5 liter",
        "qty": 0,
        "unit": "pcs",
        "type": "borrow",
        "status": "available"
    }
    
    response = requests.post(items_url, json=item_payload, headers=headers)
    
    assert response.status_code == 400
    assert "error" in response.json()
    print(f"Invalid qty rejected: {response.json()['error']}")


def test_create_user_item_invalid_type():
    """Test POST /user/items dengan type invalid"""
    access_token, username = get_access_token()
    
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    item_payload = {
        "name": "Panci Besar",
        "description": "Panci besar 5 liter",
        "qty": 2,
        "unit": "pcs",
        "type": "invalid_type",
        "status": "available"
    }
    
    response = requests.post(items_url, json=item_payload, headers=headers)
    
    assert response.status_code == 400
    assert "error" in response.json()
    print(f"Invalid type rejected: {response.json()['error']}")


def test_get_user_items_with_data():
    """Test GET /user/items setelah create item"""
    access_token, username = get_access_token()
    
    # Create 3 items
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    for i in range(3):
        item_payload = {
            "name": f"Item Test {i+1}",
            "description": f"Description {i+1}",
            "qty": i+1,
            "unit": "pcs",
            "type": "borrow" if i % 2 == 0 else "share",
            "status": "available"
        }
        response = requests.post(items_url, json=item_payload, headers=headers)
        assert response.status_code == 201
    
    # Get all items
    response = requests.get(items_url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 3
    print(f"User {username} has {len(data['items'])} items")


def test_update_user_item_success():
    """Test PUT /user/items/{id} berhasil"""
    access_token, username = get_access_token()
    
    # Create item first
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    item_payload = {
        "name": "Panci Kecil",
        "description": "Panci kecil 2 liter",
        "qty": 1,
        "unit": "pcs",
        "type": "borrow",
        "status": "available"
    }
    create_response = requests.post(items_url, json=item_payload, headers=headers)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Update item
    update_url = f"{BASE_URL}/user/items/{item_id}"
    update_payload = {
        "name": "Panci Besar 5L",
        "description": "Panci besar 5 liter stainless steel",
        "qty": 3,
        "unit": "pcs",
        "type": "borrow",
        "status": "available"
    }
    
    response = requests.put(update_url, json=update_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Panci Besar 5L"
    assert data["qty"] == 3
    assert data["remaining_qty"] == 3
    print(f"Item {item_id} updated: {data['name']}")


def test_update_user_item_not_owner():
    """Test PUT /user/items/{id} oleh bukan pemilik"""
    # User 1 create item
    access_token1, username1 = get_access_token()
    items_url = f"{BASE_URL}/user/items"
    headers1 = {"Authorization": f"Bearer {access_token1}"}
    item_payload = {
        "name": "Panci Test",
        "description": "Test panci",
        "qty": 1,
        "unit": "pcs",
        "type": "borrow",
        "status": "available"
    }
    create_response = requests.post(items_url, json=item_payload, headers=headers1)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # User 2 try to update
    access_token2, username2 = get_access_token()
    headers2 = {"Authorization": f"Bearer {access_token2}"}
    update_url = f"{BASE_URL}/user/items/{item_id}"
    update_payload = {
        "name": "Hacked Panci",
        "description": "Hacked",
        "qty": 1,
        "unit": "pcs",
        "type": "borrow",
        "status": "available"
    }
    
    response = requests.put(update_url, json=update_payload, headers=headers2)
    
    assert response.status_code == 403
    assert "error" in response.json()
    print(f"Non-owner update rejected: {response.json()['error']}")


def test_delete_user_item_success():
    """Test DELETE /user/items/{id} berhasil"""
    access_token, username = get_access_token()
    
    # Create item first
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    item_payload = {
        "name": "Item to Delete",
        "description": "Will be deleted",
        "qty": 1,
        "unit": "pcs",
        "type": "share",
        "status": "available"
    }
    create_response = requests.post(items_url, json=item_payload, headers=headers)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Delete item
    delete_url = f"{BASE_URL}/user/items/{item_id}"
    response = requests.delete(delete_url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["item_id"] == item_id
    print(f"Item {item_id} deleted successfully")


def test_delete_user_item_not_owner():
    """Test DELETE /user/items/{id} oleh bukan pemilik"""
    # User 1 create item
    access_token1, username1 = get_access_token()
    items_url = f"{BASE_URL}/user/items"
    headers1 = {"Authorization": f"Bearer {access_token1}"}
    item_payload = {
        "name": "Item Test",
        "description": "Test item",
        "qty": 1,
        "unit": "pcs",
        "type": "borrow",
        "status": "available"
    }
    create_response = requests.post(items_url, json=item_payload, headers=headers1)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # User 2 try to delete
    access_token2, username2 = get_access_token()
    headers2 = {"Authorization": f"Bearer {access_token2}"}
    delete_url = f"{BASE_URL}/user/items/{item_id}"
    
    response = requests.delete(delete_url, headers=headers2)
    
    assert response.status_code == 403
    assert "error" in response.json()
    print(f"Non-owner delete rejected: {response.json()['error']}")


def test_get_user_items_unauthorized():
    """Test GET /user/items tanpa token"""
    items_url = f"{BASE_URL}/user/items"
    response = requests.get(items_url)
    
    assert response.status_code == 401
    assert "error" in response.json()
    print(f"Unauthorized access rejected: {response.json()['error']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
