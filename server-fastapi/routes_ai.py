from fastapi import APIRouter, Depends, HTTPException, Request
from datetime import datetime
import httpx
import os
import json
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod

from models import User
from schemas import RecipeRequest, RecipeResponse
from auth import get_current_user, decode_token
from database import get_db
from config import config_manager
from decorators import log_execution_time, retry_on_failure, cache_result
from ai_proxy import ai_proxy
from ai_state import ai_state_machine, AIRequestState
from ai_observer import (
    ai_request_notifier, 
    LoggingObserver, 
    MetricsObserver, 
    WebSocketObserver,
    DatabaseObserver
)
from notifications import notification_manager
import logging
import uuid

logger = logging.getLogger(__name__)

# Initialize observers (only once)
def initialize_observers():
    """Initialize all observers for the AI notification system"""
    if ai_request_notifier.get_observer_count() == 0:
        # Attach logging observer
        ai_request_notifier.attach(LoggingObserver())
        
        # Attach metrics observer
        ai_request_notifier.attach(MetricsObserver())
        
        # Attach WebSocket observer if notifications are enabled
        if config_manager.get_bool("ENABLE_NOTIFICATIONS", True):
            ai_request_notifier.attach(WebSocketObserver(notification_manager))
        
        # Attach database observer
        # Note: This would need database session factory
        # ai_request_notifier.attach(DatabaseObserver(db_session_factory))
        
        logger.info(f"Initialized {ai_request_notifier.get_observer_count()} observers")

# Initialize observers when module loads
initialize_observers()

router = APIRouter(prefix="/ai", tags=["AI Recipe"])

# Check if AI is properly configured
def is_ai_configured() -> bool:
    """Check if Ollama AI provider is configured"""
    api_url = config_manager.get("OLLAMA_API_URL")
    model = config_manager.get("DEFAULT_OLLAMA_MODEL")
    return bool(api_url and model)

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
        factories = {
            "recipe": RecipePromptFactory()
        }
        
        factory = factories.get(prompt_type)
        if not factory:
            raise ValueError(f"Unknown prompt type: {prompt_type}")
        
        return factory

# Cookie-based authentication for AI endpoint
async def get_current_user_from_cookies_or_token(http_request: Request, db: Session = Depends(get_db)):
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
        except:
            pass

    # Fall back to Bearer token
    from fastapi.security import HTTPBearer
    security = HTTPBearer()
    try:
        credentials = await security(http_request)
        return await get_current_user(credentials, db)
    except:
        raise HTTPException(status_code=401, detail="Not authenticated")

@router.post("/recipe", response_model=RecipeResponse)
@log_execution_time
async def generate_recipe(
    request: RecipeRequest,
    current_user: User = Depends(get_current_user_from_cookies_or_token)
):
    if not request.ingredients or request.ingredients.strip() == "":
        raise HTTPException(status_code=400, detail="Ingredients cannot be empty")

    if not is_ai_configured():
        raise HTTPException(
            status_code=503,
            detail="AI service is not configured on the server"
        )
    
    # Generate unique request ID
    request_id = str(uuid.uuid4())
    
    try:
        # Use Factory Method to create prompt
        prompt_factory = AIPromptFactoryProvider.get_factory("recipe")
        prompt = prompt_factory.create_prompt(ingredients=request.ingredients)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    try:
        # Process request through state machine
        context = await ai_state_machine.process_request(
            user_id=current_user.id,
            ingredients=prompt,
            request_id=request_id
        )
        
        # Check final state
        if context.current_state == AIRequestState.COMPLETED:
            result = context.result
            
            # Parse the response content
            content = result.get("content", "")
            provider = result.get("provider", "unknown")
            
            # Try to parse JSON from response
            try:
                # Extract JSON from markdown code blocks if present
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    content = content[json_start:json_end].strip()
                
                # Try parsing the content as JSON directly
                try:
                    recipe_data = json.loads(content)
                except json.JSONDecodeError:
                    # If direct parsing fails, the content might be a JSON string that needs to be parsed again
                    # This can happen with MockProvider where content is already a JSON string
                    try:
                        # Try to parse the content as a JSON string (double parsing)
                        parsed_content = json.loads(content)
                        if isinstance(parsed_content, str):
                            # If the parsed content is still a string, parse it again
                            recipe_data = json.loads(parsed_content)
                        else:
                            recipe_data = parsed_content
                    except (json.JSONDecodeError, TypeError):
                        # If all parsing attempts fail, raise the original error
                        raise ValueError("Unable to parse JSON from response")
                
                # Validate required fields
                if not all(k in recipe_data for k in ["title", "ingredients", "instructions"]):
                    raise ValueError("Missing required fields")
                
            except (json.JSONDecodeError, ValueError):
                # Fallback to raw text if parsing fails
                recipe_data = {
                    "title": "Generated Recipe",
                    "raw_text": content,
                    "ingredients": [],
                    "instructions": [],
                    "cooking_time": "N/A",
                    "servings": "N/A",
                    "difficulty": "N/A"
                }
            
            logger.info(f"Recipe generated successfully using {provider} provider")
            
            return RecipeResponse(
                recipe=recipe_data,
                generated_at=datetime.utcnow(),
                model=result.get("model", "unknown")
            )
        else:
            # Request failed
            error_msg = context.error_message or "Unknown error occurred"
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate recipe: {error_msg}"
            )
            
    except Exception as e:
        logger.error(f"Unexpected error in recipe generation: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your request"
        )

@router.get("/request/{request_id}/status")
@log_execution_time
async def get_request_status(request_id: str, current_user: User = Depends(get_current_user_from_cookies_or_token)):
    """Get status of a specific AI request"""
    try:
        status = ai_state_machine.get_request_status(request_id)
        if not status:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Verify user owns this request
        if status.get("user_id") != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return status
    except Exception as e:
        logger.error(f"Failed to get request status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get request status")

@router.get("/requests/active")
@log_execution_time
async def get_active_requests(current_user: User = Depends(get_current_user_from_cookies_or_token)):
    """Get all active requests for current user"""
    try:
        all_requests = ai_state_machine.get_all_active_requests()
        # Filter requests for current user
        user_requests = {
            req_id: status for req_id, status in all_requests.items()
            if status.get("user_id") == current_user.id
        }
        return {"active_requests": user_requests}
    except Exception as e:
        logger.error(f"Failed to get active requests: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get active requests")

@router.delete("/request/{request_id}")
@log_execution_time
async def cancel_request(request_id: str, current_user: User = Depends(get_current_user_from_cookies_or_token)):
    """Cancel an active AI request"""
    try:
        # Check if request exists and belongs to user
        status = ai_state_machine.get_request_status(request_id)
        if not status:
            raise HTTPException(status_code=404, detail="Request not found")
        
        if status.get("user_id") != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Cancel the request
        success = ai_state_machine.cancel_request(request_id)
        if success:
            return {"message": "Request cancelled successfully"}
        else:
            raise HTTPException(status_code=400, detail="Cannot cancel completed request")
            
    except Exception as e:
        logger.error(f"Failed to cancel request: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to cancel request")

@router.get("/observers/status")
@log_execution_time
async def get_observers_status(current_user: User = Depends(get_current_user_from_cookies_or_token)):
    """Get status of all observers and recent events"""
    try:
        # Get metrics from metrics observer
        metrics_observer = None
        for observer in ai_request_notifier._observers:
            if hasattr(observer, 'get_metrics'):
                metrics_observer = observer
                break
        
        metrics = metrics_observer.get_metrics() if metrics_observer else {}
        
        # Get recent event history
        recent_events = ai_request_notifier.get_event_history(limit=50)
        
        return {
            "observer_count": ai_request_notifier.get_observer_count(),
            "observers": [obs.get_observer_id() for obs in ai_request_notifier._observers],
            "metrics": metrics,
            "recent_events": [
                {
                    "event_type": event.event_type.value,
                    "request_id": event.request_id,
                    "user_id": event.user_id,
                    "message": event.message,
                    "timestamp": event.timestamp.isoformat(),
                    "data": event.data
                }
                for event in recent_events
            ]
        }
    except Exception as e:
        logger.error(f"Failed to get observer status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get observer status")

@router.get("/metrics")
@log_execution_time
async def get_ai_metrics(current_user: User = Depends(get_current_user_from_cookies_or_token)):
    """Get AI service metrics from metrics observer"""
    try:
        # Find metrics observer
        metrics_observer = None
        for observer in ai_request_notifier._observers:
            if hasattr(observer, 'get_metrics'):
                metrics_observer = observer
                break
        
        if not metrics_observer:
            raise HTTPException(status_code=404, detail="Metrics observer not found")
        
        metrics = metrics_observer.get_metrics()
        
        # Calculate additional derived metrics
        success_rate = 0.0
        if metrics["total_requests"] > 0:
            success_rate = (metrics["completed_requests"] / metrics["total_requests"]) * 100
        
        return {
            "performance_metrics": metrics,
            "derived_metrics": {
                "success_rate_percent": round(success_rate, 2),
                "failure_rate_percent": round(100 - success_rate, 2),
                "retry_rate_percent": round((metrics["retry_count"] / max(metrics["total_requests"], 1)) * 100, 2),
                "fallback_rate_percent": round((metrics["fallback_count"] / max(metrics["total_requests"], 1)) * 100, 2)
            }
        }
    except Exception as e:
        logger.error(f"Failed to get AI metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get AI metrics")
