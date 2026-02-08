# test semua alur pengguna

import pytest
import requests
import uuid
import sys
from datetime import datetime, timedelta

# Base URL untuk API server
try:
    BASE_URL = sys.argv[1]
except IndexError:
    BASE_URL = "http://localhost:8000"


def test_alur_pengguna():
    """Test alur lengkap 2 pengguna: user1 buat items, user2 request items"""
    
    # Generate unique usernames
    user1_username = f"testuser1_{uuid.uuid4().hex[:8]}"
    user2_username = f"testuser2_{uuid.uuid4().hex[:8]}"
    password = "testpassword"
    
    print("\n=== USER 1: REGISTER & CREATE ITEMS ===")
    
    # User1 register
    print("Register user1")
    register_url = f"{BASE_URL}/auth/register"
    register_payload = {
        "username": user1_username,
        "password": password,
        "name": "Test User One",
        "address": "Jl. Test No. 1",
        "community_id": 1
    }
    register_response = requests.post(register_url, json=register_payload)
    assert register_response.status_code == 201
    user1_token = register_response.json()["access_token"]
    print(f"User1 registered: {user1_username}")
    
    # User1 logout (client-side)
    print("User1 logout (forget token)")
    user1_token = None
    
    # User1 login
    print("User1 login")
    login_url = f"{BASE_URL}/auth/login"
    login_payload = {"username": user1_username, "password": password}
    login_response = requests.post(login_url, json=login_payload)
    assert login_response.status_code == 200
    user1_token = login_response.json()["access_token"]
    print(f"User1 logged in, token: {user1_token[:20]}...")
    
    # User1 check /user/items (should be empty)
    print("User1 check /user/items (should be empty)")
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {user1_token}"}
    response = requests.get(items_url, headers=headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) == 0
    print("User1 items: 0 (empty)")
    
    # User1 create 30 items (loop)
    print("User1 create 30 items (loop)")
    created_items = []
    for i in range(30):
        item_payload = {
            "name": f"Test Item {i+1}",
            "description": f"Description for test item {i+1}",
            "qty": 10,
            "unit": "pcs",
            "type": "borrow" if i % 2 == 0 else "share",
            "status": "available"
        }
        response = requests.post(items_url, json=item_payload, headers=headers)
        assert response.status_code == 201
        created_items.append(response.json()["id"])
    print(f"User1 created 30 items, IDs: {created_items[0]}-{created_items[-1]}")
    
    # User1 logout
    print("User1 logout (forget token)")
    user1_token = None
    
    print("\n=== USER 2: REGISTER & REQUEST ITEMS ===")
    
    # User2 register
    print("Register user2")
    register_payload = {
        "username": user2_username,
        "password": password,
        "name": "Test User Two",
        "address": "Jl. Test No. 2"
    }
    register_response = requests.post(register_url, json=register_payload)
    assert register_response.status_code == 201
    user2_token = register_response.json()["access_token"]
    print(f"User2 registered: {user2_username}")
    
    # User2 open homepage /items (no filter)
    print("User2 open homepage /items (no filter)")
    items_url = f"{BASE_URL}/items"
    headers = {"Authorization": f"Bearer {user2_token}"}
    response = requests.get(items_url, headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(f"Homepage page 1: {len(data['items'])} items, total pages: {data['pagination']['total_pages']}")
    
    # User2 request page 2
    print("User2 request page 2")
    response = requests.get(f"{items_url}?page=2", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(f"Homepage page 2: {len(data['items'])} items")
    
    # User2 search items (keyword: 'Test Item 1')
    print("User2 search items (keyword: 'Test Item 1')")
    response = requests.get(f"{items_url}?search=Test Item 1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    print(f"Search result: {len(data['items'])} items found")
    
    # User2 make outgoing request to first item
    print("User2 make outgoing request to first item")
    first_item_id = created_items[0]
    request_url = f"{BASE_URL}/items/{first_item_id}/request"
    
    # Generate dynamic future dates
    date_start = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    date_end = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d')

    request_payload = {
        "requested_qty": 5,
        "date_start": date_start,
        "date_end": date_end
    }
    response = requests.post(request_url, json=request_payload, headers=headers)
    assert response.status_code == 201
    request_id = response.json()["request_id"]
    print(f"User2 created request ID: {request_id}, status: {response.json()['status']}")
    
    print("\n=== USER 1: APPROVE REQUEST ===")
    
    # User1 login again
    print("User1 login again")
    login_response = requests.post(login_url, json={"username": user1_username, "password": password})
    assert login_response.status_code == 200
    user1_token = login_response.json()["access_token"]
    
    # User1 check incoming requests
    print("User1 check incoming requests")
    headers = {"Authorization": f"Bearer {user1_token}"}
    requests_url = f"{BASE_URL}/user/requests?type=incoming"
    response = requests.get(requests_url, headers=headers)
    assert response.status_code == 200
    incoming_requests = response.json()["requests"]
    print(f"User1 incoming requests: {len(incoming_requests)}")
    
    # User1 approve request
    print(f"User1 approve request {request_id}")
    approve_url = f"{BASE_URL}/user/requests/{request_id}"
    approve_payload = {"status": "approved"}
    response = requests.patch(approve_url, json=approve_payload, headers=headers)
    assert response.status_code == 200
    print(f"Request {request_id} approved, new status: {response.json()['status']}")
    
    print("\n=== CLEANUP ===")
    
    # Delete user1 (cascade delete items & requests)
    print(f"Delete user1: {user1_username}")
    delete_url = f"{BASE_URL}/dev/delete/user/{user1_username}"
    response = requests.delete(delete_url, headers=headers)
    if response.status_code == 200:
        print(f"User1 deleted: {response.json()['deleted_items']} items, {response.json()['deleted_requests']} requests")
    
    # Delete user2
    print(f"Delete user2: {user2_username}")
    headers = {"Authorization": f"Bearer {user2_token}"}
    delete_url = f"{BASE_URL}/dev/delete/user/{user2_username}"
    response = requests.delete(delete_url, headers=headers)
    if response.status_code == 200:
        print(f"User2 deleted")
    
    
    print("\n=== Test alur pengguna lengkap berhasil! ===")
    
    return {
        "user1_username": user1_username,
        "user2_username": user2_username,
        "created_items": created_items,
        "request_id": request_id
    }


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])  # -s untuk menampilkan print statements
