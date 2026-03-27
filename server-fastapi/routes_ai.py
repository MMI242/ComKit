from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime
import json
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

from models import User
from schemas import RecipeRequest, RecipeResponse
from auth import get_current_user, decode_token
from database import get_db
from config import config_manager
from decorators import log_execution_time, retry_on_failure, cache_result

router = APIRouter(prefix="/ai", tags=["AI Recipe"])

def _load_ollama_config():
    """Reload Ollama config from .env file on every call"""
    from dotenv import dotenv_values
    env = dotenv_values(".env")
    url = (env.get("OLLAMA_API_URL") or config_manager.get("OLLAMA_API_URL", "https://ollama.com")).rstrip("/")
    key = env.get("OLLAMA_API_KEY") or config_manager.get("OLLAMA_API_KEY")
    model = (
        env.get("DEFAULT_OLLAMA_MODEL")
        or env.get("OLLAMA_DEFAULT_MODEL")
        or config_manager.get("DEFAULT_OLLAMA_MODEL")
        or config_manager.get("OLLAMA_DEFAULT_MODEL")
    )
    return url, key, model


# Abstract Factory for AI prompt generation
class AIPromptFactory(ABC):
    """Abstract base class for AI prompt factories"""

    @abstractmethod
    def create_prompt(self, **kwargs) -> str:
        """Create a prompt with given parameters"""
        pass


class RecipePromptFactory(AIPromptFactory):
    """Factory for creating recipe generation prompts"""

    def create_prompt(self, **kwargs) -> str:
        """Create a recipe generation prompt"""
        ingredients = kwargs.get("ingredients", "")
        return f"""Generate a recipe using these ingredients: {ingredients}

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


class AIPromptFactoryProvider:
    """Provider class to manage AI prompt factories"""

    @staticmethod
    def get_factory(prompt_type: str) -> AIPromptFactory:
        """Get the appropriate factory for the prompt type"""
        factories = {"recipe": RecipePromptFactory()}

        factory = factories.get(prompt_type)
        if not factory:
            raise ValueError(f"Unknown prompt type: {prompt_type}")

        return factory


# Cookie-based authentication for AI endpoint
async def get_current_user_from_cookies_or_token(
    http_request: Request, db: Session = Depends(get_db)
):
    # First try to get user from cookies
    access_token = http_request.cookies.get("access_token")
    if access_token:
        try:
            payload = decode_token(access_token)
            user_id = payload.get("user_id")

            if user_id:
                user = db.query(User).filter(User.id == user_id).first()
                if user:
                    return user
        except Exception:
            pass

    # Fall back to Bearer token
    from fastapi.security import HTTPBearer

    security = HTTPBearer()
    try:
        credentials = await security(http_request)
        return await get_current_user(credentials, db)
    except Exception:
        raise HTTPException(status_code=401, detail="Not authenticated")


@router.post("/recipe", response_model=RecipeResponse)
@log_execution_time
@retry_on_failure(max_retries=2, delay_seconds=0.5)
async def generate_recipe(
    request: RecipeRequest,
    current_user: User = Depends(get_current_user_from_cookies_or_token),
):
    if not request.ingredients or request.ingredients.strip() == "":
        raise HTTPException(status_code=400, detail="Ingredients cannot be empty")

    OLLAMA_API_URL, OLLAMA_API_KEY, DEFAULT_OLLAMA_MODEL = _load_ollama_config()

    if not DEFAULT_OLLAMA_MODEL:
        raise HTTPException(
            status_code=503,
            detail="AI model is not configured on the server"
        )
    
    # Use Factory Method to create prompt
    try:
        prompt_factory = AIPromptFactoryProvider.get_factory("recipe")
        prompt = prompt_factory.create_prompt(ingredients=request.ingredients)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))

    try:
        import ollama

        headers = {}
        if OLLAMA_API_KEY:
            headers["Authorization"] = f"Bearer {OLLAMA_API_KEY}"

        print(f"[OLLAMA] URL={OLLAMA_API_URL} Model={DEFAULT_OLLAMA_MODEL}", flush=True)
        print(f"[OLLAMA] PROMPT: {prompt}", flush=True)

        client = ollama.AsyncClient(host=OLLAMA_API_URL, headers=headers)
        result = await client.generate(
            model=DEFAULT_OLLAMA_MODEL,
            prompt=prompt,
            stream=False
        )

        ai_response = result.get("response", "")
        print(f"[OLLAMA] RESPONSE: {ai_response}", flush=True)

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
            generated_at=datetime.utcnow(),
            model=DEFAULT_OLLAMA_MODEL
        )

    except Exception as e:
        print(f"[OLLAMA] ERROR: {e}", flush=True)
        raise HTTPException(
            status_code=503,
            detail=f"AI service error: {str(e)}"
        )
