import os
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger(__name__)


class ConfigManager:
    """Singleton class for managing application configuration and environment variables"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if not ConfigManager._initialized:
            self._config_cache: Dict[str, Any] = {}
            ConfigManager._initialized = True
            logger.info("ConfigManager singleton initialized")

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value with caching"""
        if key in self._config_cache:
            return self._config_cache[key]

        value = os.getenv(key, default)
        self._config_cache[key] = value
        return value

    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean configuration value"""
        if key in self._config_cache:
            return self._config_cache[key]

        value = os.getenv(key, str(default)).lower()
        bool_value = value in ("true", "1", "yes", "on")
        self._config_cache[key] = bool_value
        return bool_value

    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer configuration value"""
        if key in self._config_cache:
            return self._config_cache[key]

        try:
            value = int(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            value = default
            logger.warning(f"Invalid integer value for {key}, using default: {default}")

        self._config_cache[key] = value
        return value

    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get float configuration value"""
        if key in self._config_cache:
            return self._config_cache[key]

        try:
            value = float(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            value = default
            logger.warning(f"Invalid float value for {key}, using default: {default}")

        self._config_cache[key] = value
        return value

    def get_list(self, key: str, separator: str = ",", default: list = None) -> list:
        """Get list configuration value"""
        if key in self._config_cache:
            return self._config_cache[key]

        if default is None:
            default = []

        value = os.getenv(key, "")
        if not value:
            self._config_cache[key] = default
            return default

        list_value = [item.strip() for item in value.split(separator) if item.strip()]
        self._cache[key] = list_value
        return list_value

    def set(self, key: str, value: Any) -> None:
        """Set configuration value (for runtime changes)"""
        self._config_cache[key] = value

    def clear_cache(self, key: Optional[str] = None) -> None:
        """Clear configuration cache"""
        if key:
            self._config_cache.pop(key, None)
        else:
            self._config_cache.clear()

    def get_all_config(self) -> Dict[str, Any]:
        """Get all configuration values (for debugging)"""
        return {
            "ENVIRONMENT": self.get("ENVIRONMENT", "production"),
            "ENABLE_NOTIFICATIONS": self.get_bool("ENABLE_NOTIFICATIONS", True),
            "OLLAMA_API_URL": self.get("OLLAMA_API_URL", "https://api.ollama.com"),
            "DEFAULT_OLLAMA_MODEL": self.get("DEFAULT_OLLAMA_MODEL"),
            "CORS_ALLOWED_ORIGINS": self.get_list("CORS_ALLOWED_ORIGINS"),
        }


# Singleton instance
config_manager = ConfigManager()
