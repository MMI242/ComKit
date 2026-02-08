# test AI recipe generation

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
        "address": "Jl. Test No. 123"
    }
    response = requests.post(register_url, json=register_payload)
    assert response.status_code == 201
    return response.json()["access_token"], username


def test_generate_recipe_success():
    """Test POST /ai/recipe berhasil generate resep"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {
        "ingredients": "ayam, bawang putih, jahe, kecap manis, minyak goreng"
    }
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "recipe" in data
    assert "generated_at" in data
    
    recipe = data["recipe"]
    assert "title" in recipe
    assert "ingredients" in recipe
    assert "instructions" in recipe
    
    print(f"Recipe generated: {recipe['title']}")
    print(f"Ingredients: {len(recipe['ingredients'])} items")
    print(f"Instructions: {len(recipe['instructions'])} steps")


def test_generate_recipe_simple_ingredients():
    """Test POST /ai/recipe dengan bahan sederhana"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {
        "ingredients": "telur, garam, minyak"
    }
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "recipe" in data
    
    print(f"Simple recipe: {data['recipe']['title']}")


def test_generate_recipe_long_ingredients():
    """Test POST /ai/recipe dengan banyak bahan"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {
        "ingredients": "ayam, bawang merah, bawang putih, cabai merah, cabai rawit, tomat, kemiri, kunyit, jahe, lengkuas, serai, daun salam, daun jeruk, santan, garam, gula, minyak goreng"
    }
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "recipe" in data
    
    print(f"Complex recipe: {data['recipe']['title']}")


def test_generate_recipe_empty_ingredients():
    """Test POST /ai/recipe dengan ingredients kosong"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {
        "ingredients": ""
    }
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 400
    assert "error" in response.json()
    print(f"Empty ingredients rejected: {response.json()['error']}")


def test_generate_recipe_missing_ingredients():
    """Test POST /ai/recipe tanpa field ingredients"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {}
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 400
    assert "error" in response.json()
    print(f"Missing ingredients rejected: {response.json()['error']}")


def test_generate_recipe_unauthorized():
    """Test POST /ai/recipe tanpa token"""
    recipe_url = f"{BASE_URL}/ai/recipe"
    recipe_payload = {
        "ingredients": "telur, garam"
    }
    
    response = requests.post(recipe_url, json=recipe_payload)
    
    assert response.status_code == 401
    assert "error" in response.json()
    print(f"Unauthorized access rejected: {response.json()['error']}")


def test_generate_recipe_with_special_ingredients():
    """Test POST /ai/recipe dengan bahan khas Indonesia"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {
        "ingredients": "tempe, tahu, kacang panjang, cabai, kecap manis, bawang putih"
    }
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "recipe" in data
    
    print(f"Indonesian recipe: {data['recipe']['title']}")


def test_generate_recipe_with_meat():
    """Test POST /ai/recipe dengan daging"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {
        "ingredients": "daging sapi, kentang, wortel, bawang bombay, tomat"
    }
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "recipe" in data
    
    print(f"Meat recipe: {data['recipe']['title']}")


def test_generate_recipe_vegetarian():
    """Test POST /ai/recipe vegetarian"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {
        "ingredients": "bayam, jagung, wortel, buncis, kentang, bawang putih"
    }
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert "recipe" in data
    
    print(f"Vegetarian recipe: {data['recipe']['title']}")


def test_generate_recipe_response_structure():
    """Test POST /ai/recipe validasi struktur response lengkap"""
    access_token, username = get_access_token()
    
    recipe_url = f"{BASE_URL}/ai/recipe"
    headers = {"Authorization": f"Bearer {access_token}"}
    recipe_payload = {
        "ingredients": "ikan, tomat, bawang merah, cabai"
    }
    
    response = requests.post(recipe_url, json=recipe_payload, headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    
    # Validate top level
    assert "recipe" in data
    assert "generated_at" in data
    
    recipe = data["recipe"]
    
    # Validate recipe structure
    assert "title" in recipe
    assert "ingredients" in recipe
    assert "instructions" in recipe
    
    # Optional fields (might exist)
    optional_fields = ["cooking_time", "servings", "difficulty", "raw_text"]
    
    # Validate types
    assert isinstance(recipe["title"], str)
    assert isinstance(recipe["ingredients"], list)
    assert isinstance(recipe["instructions"], list)
    
    if "cooking_time" in recipe:
        assert isinstance(recipe["cooking_time"], str)
    if "servings" in recipe:
        assert isinstance(recipe["servings"], str)
    if "difficulty" in recipe:
        assert isinstance(recipe["difficulty"], str)
    
    print(f"Recipe structure valid: {recipe['title']}")
    print(f"Has {len(recipe['ingredients'])} ingredients")
    print(f"Has {len(recipe['instructions'])} steps")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
