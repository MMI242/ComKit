from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
import httpx
import os
from dotenv import load_dotenv
import json

from models import User
from schemas import RecipeRequest, RecipeResponse
from auth import get_current_user

load_dotenv()

router = APIRouter(prefix="/ai", tags=["AI Recipe"])

OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")

@router.post("/recipe", response_model=RecipeResponse)
async def generate_recipe(
    request: RecipeRequest,
    current_user: User = Depends(get_current_user)
):
    if not request.ingredients or request.ingredients.strip() == "":
        raise HTTPException(status_code=400, detail="Ingredients cannot be empty")
    
    # Prepare prompt for Ollama
    prompt = f"""Generate a recipe using these ingredients: {request.ingredients}

Please provide the recipe in the following JSON format:
{{
    "title": "Recipe Name",
    "ingredients": ["ingredient 1", "ingredient 2", ...],
    "instructions": ["step 1", "step 2", ...],
    "cooking_time": "time in minutes",
    "servings": "number of servings",
    "difficulty": "easy|medium|hard"
}}

Only respond with valid JSON, no additional text."""
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{OLLAMA_API_URL}/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False
                }
            )
            
            if response.status_code != 200:
                # Try with mistral as fallback
                response = await client.post(
                    f"{OLLAMA_API_URL}/api/generate",
                    json={
                        "model": "mistral",
                        "prompt": prompt,
                        "stream": False
                    }
                )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=503,
                    detail="AI service temporarily unavailable. Please try again later"
                )
            
            result = response.json()
            ai_response = result.get("response", "")
            
            # Try to parse JSON from response
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in ai_response:
                    json_start = ai_response.find("```json") + 7
                    json_end = ai_response.find("```", json_start)
                    ai_response = ai_response[json_start:json_end].strip()
                elif "```" in ai_response:
                    json_start = ai_response.find("```") + 3
                    json_end = ai_response.find("```", json_start)
                    ai_response = ai_response[json_start:json_end].strip()
                
                recipe_data = json.loads(ai_response)
                
                # Validate required fields
                if not all(k in recipe_data for k in ["title", "ingredients", "instructions"]):
                    raise ValueError("Missing required fields")
                
            except (json.JSONDecodeError, ValueError):
                # Fallback to raw text if parsing fails
                recipe_data = {
                    "title": "Generated Recipe",
                    "raw_text": ai_response,
                    "ingredients": [],
                    "instructions": [],
                    "cooking_time": "N/A",
                    "servings": "N/A",
                    "difficulty": "N/A"
                }
            
            return RecipeResponse(
                recipe=recipe_data,
                generated_at=datetime.utcnow()
            )
            
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=503,
            detail="AI service temporarily unavailable. Please try again later"
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="AI service temporarily unavailable. Please try again later"
        )
