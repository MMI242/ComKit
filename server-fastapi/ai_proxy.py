import httpx
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from config import config_manager
from decorators import log_execution_time, retry_on_failure, cache_result

logger = logging.getLogger(__name__)

class AIProvider(ABC):
    """Abstract base class for AI service providers"""
    
    @abstractmethod
    async def generate_recipe(self, ingredients: str, model: str) -> Dict[str, Any]:
        """Generate a recipe using the AI provider"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the AI provider is available"""
        pass
    
    @abstractmethod
    def get_available_models(self) -> list[str]:
        """Get list of available models"""
        pass

class OllamaProvider(AIProvider):
    """Concrete implementation for Ollama AI provider"""
    
    def __init__(self):
        self.api_url = config_manager.get("OLLAMA_API_URL", "https://api.ollama.com").rstrip("/")
        self.api_key = config_manager.get("OLLAMA_API_KEY")
        self.default_model = (
            config_manager.get("DEFAULT_OLLAMA_MODEL")
            or config_manager.get("OLLAMA_DEFAULT_MODEL")
        )
    
    @log_execution_time
    @retry_on_failure(max_retries=2, delay_seconds=1.0)
    async def generate_recipe(self, ingredients: str, model: str) -> Dict[str, Any]:
        """Generate recipe using Ollama API"""
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        
        payload = {
            "model": model or self.default_model,
            "prompt": ingredients,
            "stream": False
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/api/generate",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama API error: {e.response.status_code} - {e.response.text}")
            raise
        except Exception as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            raise
    
    async def health_check(self) -> bool:
        """Check if Ollama service is healthy"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.api_url}/api/tags")
                return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama health check failed: {str(e)}")
            return False
    
    def get_available_models(self) -> list[str]:
        """Get available models from Ollama"""
        # This would typically make an API call to /api/tags
        # For now, return common models
        return ["qwen3:8b", "llama2", "mistral", "codellama"]

class OpenAIProvider(AIProvider):
    """Alternative AI provider (for fallback)"""
    
    def __init__(self):
        self.api_key = config_manager.get("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1"
        self.default_model = "gpt-3.5-turbo"
    
    @log_execution_time
    @retry_on_failure(max_retries=2, delay_seconds=1.0)
    async def generate_recipe(self, ingredients: str, model: str) -> Dict[str, Any]:
        """Generate recipe using OpenAI API"""
        if not self.api_key:
            raise ValueError("OpenAI API key not configured")
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model or self.default_model,
            "messages": [
                {"role": "system", "content": "You are a helpful chef assistant. Generate recipes based on available ingredients."},
                {"role": "user", "content": ingredients}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def health_check(self) -> bool:
        """Check if OpenAI service is healthy"""
        return bool(self.api_key)
    
    def get_available_models(self) -> list[str]:
        """Get available OpenAI models"""
        return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]

class AIProxy:
    """Proxy class that manages multiple AI providers and provides unified interface"""
    
    def __init__(self):
        self.providers = {
            "ollama": OllamaProvider(),
            "openai": OpenAIProvider()
        }
        self.primary_provider = "ollama"
        self.fallback_providers = ["openai"]
        self._health_cache = {}
        self._cache_ttl = 300  # 5 minutes
    
    @log_execution_time
    @cache_result(ttl_seconds=300, max_size=100)
    async def generate_recipe(self, ingredients: str, model: Optional[str] = None, provider: Optional[str] = None) -> Dict[str, Any]:
        """Generate recipe using available providers with fallback"""
        
        # Determine which provider to use
        target_provider = provider or self.primary_provider
        
        # Try primary provider first
        if target_provider in self.providers:
            try:
                if await self._is_provider_healthy(target_provider):
                    logger.info(f"Using {target_provider} provider")
                    result = await self.providers[target_provider].generate_recipe(ingredients, model or "")
                    return self._normalize_response(result, target_provider)
                else:
                    logger.warning(f"Provider {target_provider} is unhealthy, trying fallbacks")
            except Exception as e:
                logger.error(f"Primary provider {target_provider} failed: {str(e)}")
        
        # Try fallback providers
        for fallback_provider in self.fallback_providers:
            if fallback_provider in self.providers and await self._is_provider_healthy(fallback_provider):
                try:
                    logger.info(f"Using fallback provider {fallback_provider}")
                    result = await self.providers[fallback_provider].generate_recipe(ingredients, model or "")
                    return self._normalize_response(result, fallback_provider)
                except Exception as e:
                    logger.error(f"Fallback provider {fallback_provider} failed: {str(e)}")
                    continue
        
        # All providers failed
        raise Exception("All AI providers are unavailable or failed to generate recipe")
    
    async def _is_provider_healthy(self, provider_name: str) -> bool:
        """Check provider health with caching"""
        current_time = asyncio.get_event_loop().time()
        
        # Check cache
        if provider_name in self._health_cache:
            cached_time, cached_health = self._health_cache[provider_name]
            if current_time - cached_time < self._cache_ttl:
                return cached_health
        
        # Perform health check
        provider = self.providers.get(provider_name)
        if provider:
            health = await provider.health_check()
            self._health_cache[provider_name] = (current_time, health)
            return health
        
        return False
    
    def _normalize_response(self, response: Dict[str, Any], provider: str) -> Dict[str, Any]:
        """Normalize response format across different providers"""
        if provider == "ollama":
            return {
                "content": response.get("response", ""),
                "model": response.get("model", ""),
                "provider": "ollama",
                "raw": response
            }
        elif provider == "openai":
            content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {
                "content": content,
                "model": response.get("model", ""),
                "provider": "openai",
                "raw": response
            }
        else:
            return response
    
    @log_execution_time
    async def get_provider_status(self) -> Dict[str, Any]:
        """Get status of all providers"""
        status = {}
        for name, provider in self.providers.items():
            status[name] = {
                "healthy": await self._is_provider_healthy(name),
                "models": provider.get_available_models()
            }
        return status
    
    def get_available_providers(self) -> list[str]:
        """Get list of available providers"""
        return list(self.providers.keys())
    
    def set_primary_provider(self, provider_name: str) -> bool:
        """Set primary provider"""
        if provider_name in self.providers:
            self.primary_provider = provider_name
            logger.info(f"Primary provider set to {provider_name}")
            return True
        return False
    
    @cache_result(ttl_seconds=3600, max_size=50)
    async def get_available_models(self) -> Dict[str, list[str]]:
        """Get available models from all providers"""
        models = {}
        for name, provider in self.providers.items():
            if await self._is_provider_healthy(name):
                models[name] = provider.get_available_models()
        return models

# Global proxy instance
ai_proxy = AIProxy()
