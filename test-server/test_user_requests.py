# test user requests (incoming/outgoing) dan update status

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


def create_item(access_token, name="Test Item"):
    """Helper untuk create item"""
    items_url = f"{BASE_URL}/user/items"
    headers = {"Authorization": f"Bearer {access_token}"}
    item_payload = {
        "name": name,
        "description": f"Description for {name}",
        "qty": 10,
        "unit": "pcs",
        "type": "borrow",
        "status": "available"
    }
    response = requests.post(items_url, json=item_payload, headers=headers)
    assert response.status_code == 201
    return response.json()["id"]


def test_get_incoming_requests_empty():
    """Test GET /user/requests?type=incoming saat belum ada request"""
    access_token, username = get_access_token()
    
    requests_url = f"{BASE_URL}/user/requests?type=incoming"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(requests_url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "requests" in data
    assert len(data["requests"]) == 0
    print(f"User {username} has 0 incoming requests")


def test_get_outgoing_requests_empty():
    """Test GET /user/requests?type=outgoing saat belum ada request"""
    access_token, username = get_access_token()
    
    requests_url = f"{BASE_URL}/user/requests?type=outgoing"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(requests_url, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "requests" in data
    assert len(data["requests"]) == 0
    print(f"User {username} has 0 outgoing requests")


def test_get_requests_invalid_type():
    """Test GET /user/requests dengan type invalid"""
    access_token, username = get_access_token()
    
    requests_url = f"{BASE_URL}/user/requests?type=invalid"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(requests_url, headers=headers)
    
    assert response.status_code == 400
    assert "error" in response.json()
    print(f"Invalid type rejected: {response.json()['error']}")


def test_get_incoming_requests_with_data():
    """Test GET /user/requests?type=incoming setelah ada request masuk"""
    # User 1 (owner) create item
    token1, user1 = get_access_token()
    item_id = create_item(token1, "Item Owner")
    
    # User 2 (requester) request item
    token2, user2 = get_access_token()
    request_url = f"{BASE_URL}/items/{item_id}/request"
    headers2 = {"Authorization": f"Bearer {token2}"}
    request_payload = {
        "requested_qty": 5,
        "date_start": "2025-01-20",
        "date_end": "2025-01-22"
    }
    response = requests.post(request_url, json=request_payload, headers=headers2)
    assert response.status_code == 201
    
    # User 1 check incoming requests
    requests_url = f"{BASE_URL}/user/requests?type=incoming"
    headers1 = {"Authorization": f"Bearer {token1}"}
    response = requests.get(requests_url, headers=headers1)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["requests"]) == 1
    req = data["requests"][0]
    assert req["status"] == "pending"
    assert req["requested_qty"] == 5
    assert "requester" in req
    assert "item" in req
    print(f"User {user1} has 1 incoming request: {req['id']}")


def test_get_outgoing_requests_with_data():
    """Test GET /user/requests?type=outgoing setelah buat request"""
    # User 1 (owner) create item
    token1, user1 = get_access_token()
    item_id = create_item(token1, "Item Owner")
    
    # User 2 (requester) request item
    token2, user2 = get_access_token()
    request_url = f"{BASE_URL}/items/{item_id}/request"
    headers2 = {"Authorization": f"Bearer {token2}"}
    request_payload = {
        "requested_qty": 5,
        "date_start": "2025-01-20",
        "date_end": "2025-01-22"
    }
    response = requests.post(request_url, json=request_payload, headers=headers2)
    assert response.status_code == 201
    
    # User 2 check outgoing requests
    requests_url = f"{BASE_URL}/user/requests?type=outgoing"
    response = requests.get(requests_url, headers=headers2)
    
    assert response.status_code == 200
    data = response.json()
    assert len(data["requests"]) == 1
    req = data["requests"][0]
    assert req["status"] == "pending"
    assert req["requested_qty"] == 5
    assert "owner" in req
    assert "item" in req
    print(f"User {user2} has 1 outgoing request: {req['id']}")


def test_approve_request_by_owner():
    """Test PATCH /user/requests/{id} approve by owner"""
    # User 1 (owner) create item
    token1, user1 = get_access_token()
    item_id = create_item(token1, "Item Owner")
    
    # User 2 (requester) request item
    token2, user2 = get_access_token()
    request_url = f"{BASE_URL}/items/{item_id}/request"
    headers2 = {"Authorization": f"Bearer {token2}"}
    request_payload = {
        "requested_qty": 5,
        "date_start": "2025-01-20",
        "date_end": "2025-01-22"
    }
    response = requests.post(request_url, json=request_payload, headers=headers2)
    assert response.status_code == 201
    request_id = response.json()["request_id"]
    
    # User 1 approve request
    update_url = f"{BASE_URL}/user/requests/{request_id}"
    headers1 = {"Authorization": f"Bearer {token1}"}
    update_payload = {"status": "approved"}
    response = requests.patch(update_url, json=update_payload, headers=headers1)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"
    print(f"Request {request_id} approved by owner")


def test_reject_request_by_owner():
    """Test PATCH /user/requests/{id} reject by owner"""
    # User 1 (owner) create item
    token1, user1 = get_access_token()
    item_id = create_item(token1, "Item Owner")
    
    # User 2 (requester) request item
    token2, user2 = get_access_token()
    request_url = f"{BASE_URL}/items/{item_id}/request"
    headers2 = {"Authorization": f"Bearer {token2}"}
    request_payload = {
        "requested_qty": 5,
        "date_start": "2025-01-20",
        "date_end": "2025-01-22"
    }
    response = requests.post(request_url, json=request_payload, headers=headers2)
    assert response.status_code == 201
    request_id = response.json()["request_id"]
    
    # User 1 reject request
    update_url = f"{BASE_URL}/user/requests/{request_id}"
    headers1 = {"Authorization": f"Bearer {token1}"}
    update_payload = {"status": "rejected"}
    response = requests.patch(update_url, json=update_payload, headers=headers1)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rejected"
    print(f"Request {request_id} rejected by owner")


def test_cancel_request_by_requester():
    """Test PATCH /user/requests/{id} cancel by requester"""
    # User 1 (owner) create item
    token1, user1 = get_access_token()
    item_id = create_item(token1, "Item Owner")
    
    # User 2 (requester) request item
    token2, user2 = get_access_token()
    request_url = f"{BASE_URL}/items/{item_id}/request"
    headers2 = {"Authorization": f"Bearer {token2}"}
    request_payload = {
        "requested_qty": 5,
        "date_start": "2025-01-20",
        "date_end": "2025-01-22"
    }
    response = requests.post(request_url, json=request_payload, headers=headers2)
    assert response.status_code == 201
    request_id = response.json()["request_id"]
    
    # User 2 cancel request
    update_url = f"{BASE_URL}/user/requests/{request_id}"
    update_payload = {"status": "cancelled"}
    response = requests.patch(update_url, json=update_payload, headers=headers2)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "cancelled"
    print(f"Request {request_id} cancelled by requester")


def test_returned_request_by_owner():
    """Test PATCH /user/requests/{id} returned by owner"""
    # User 1 (owner) create item
    token1, user1 = get_access_token()
    item_id = create_item(token1, "Item Owner")
    
    # User 2 (requester) request item
    token2, user2 = get_access_token()
    request_url = f"{BASE_URL}/items/{item_id}/request"
    headers2 = {"Authorization": f"Bearer {token2}"}
    request_payload = {
        "requested_qty": 5,
        "date_start": "2025-01-20",
        "date_end": "2025-01-22"
    }
    response = requests.post(request_url, json=request_payload, headers=headers2)
    assert response.status_code == 201
    request_id = response.json()["request_id"]
    
    # User 1 approve request
    update_url = f"{BASE_URL}/user/requests/{request_id}"
    headers1 = {"Authorization": f"Bearer {token1}"}
    update_payload = {"status": "approved"}
    response = requests.patch(update_url, json=update_payload, headers=headers1)
    assert response.status_code == 200
    
    # User 1 mark as returned
    update_payload = {"status": "returned"}
    response = requests.patch(update_url, json=update_payload, headers=headers1)
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "returned"
    print(f"Request {request_id} marked as returned by owner")


def test_update_request_unauthorized():
    """Test PATCH /user/requests/{id} oleh user lain (bukan owner/requester)"""
    # User 1 (owner) create item
    token1, user1 = get_access_token()
    item_id = create_item(token1, "Item Owner")
    
    # User 2 (requester) request item
    token2, user2 = get_access_token()
    request_url = f"{BASE_URL}/items/{item_id}/request"
    headers2 = {"Authorization": f"Bearer {token2}"}
    request_payload = {
        "requested_qty": 5,
        "date_start": "2025-01-20",
        "date_end": "2025-01-22"
    }
    response = requests.post(request_url, json=request_payload, headers=headers2)
    assert response.status_code == 201
    request_id = response.json()["request_id"]
    
    # User 3 (random user) try to update
    token3, user3 = get_access_token()
    headers3 = {"Authorization": f"Bearer {token3}"}
    update_url = f"{BASE_URL}/user/requests/{request_id}"
    update_payload = {"status": "approved"}
    response = requests.patch(update_url, json=update_payload, headers=headers3)
    
    assert response.status_code == 403
    assert "error" in response.json()
    print(f"Unauthorized user update rejected: {response.json()['error']}")


def test_update_request_invalid_status():
    """Test PATCH /user/requests/{id} dengan status invalid"""
    # User 1 (owner) create item
    token1, user1 = get_access_token()
    item_id = create_item(token1, "Item Owner")
    
    # User 2 (requester) request item
    token2, user2 = get_access_token()
    request_url = f"{BASE_URL}/items/{item_id}/request"
    headers2 = {"Authorization": f"Bearer {token2}"}
    request_payload = {
        "requested_qty": 5,
        "date_start": "2025-01-20",
        "date_end": "2025-01-22"
    }
    response = requests.post(request_url, json=request_payload, headers=headers2)
    assert response.status_code == 201
    request_id = response.json()["request_id"]
    
    # Try invalid status transition (pending -> returned, skip approved)
    update_url = f"{BASE_URL}/user/requests/{request_id}"
    headers1 = {"Authorization": f"Bearer {token1}"}
    update_payload = {"status": "returned"}
    response = requests.patch(update_url, json=update_payload, headers=headers1)
    
    assert response.status_code == 400
    assert "error" in response.json()
    print(f"Invalid status transition rejected: {response.json()['error']}")


def test_get_requests_unauthorized():
    """Test GET /user/requests tanpa token"""
    requests_url = f"{BASE_URL}/user/requests?type=incoming"
    response = requests.get(requests_url)
    
    assert response.status_code == 401
    assert "error" in response.json()
    print(f"Unauthorized access rejected: {response.json()['error']}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
