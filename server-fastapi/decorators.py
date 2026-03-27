import functools
import logging
import time
from typing import Any, Callable, Dict, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def log_execution_time(func: Callable) -> Callable:
    """Decorator to log execution time of functions"""

    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"{func.__name__} failed after {execution_time:.4f}s: {str(e)}"
            )
            raise

    @functools.wraps(func)
    def sync_wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.4f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(
                f"{func.__name__} failed after {execution_time:.4f}s: {str(e)}"
            )
            raise

    # Return appropriate wrapper based on whether function is async
    if asyncio.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper


def cache_result(ttl_seconds: int = 300, max_size: int = 100) -> Callable:
    """Decorator to cache function results with TTL"""

    def decorator(func: Callable) -> Callable:
        cache: Dict[str, Dict[str, Any]] = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = (
                f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            )
            current_time = time.time()

            # Check if cache exists and is not expired
            if cache_key in cache:
                cache_entry = cache[cache_key]
                if current_time - cache_entry["timestamp"] < ttl_seconds:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cache_entry["result"]
                else:
                    # Remove expired entry
                    del cache[cache_key]

            # Execute function and cache result
            result = func(*args, **kwargs)

            # Implement LRU cache size limit
            if len(cache) >= max_size:
                # Remove oldest entry
                oldest_key = min(cache.keys(), key=lambda k: cache[k]["timestamp"])
                del cache[oldest_key]

            cache[cache_key] = {"result": result, "timestamp": current_time}

            logger.debug(f"Cached result for {func.__name__}")
            return result

        # Add cache management methods
        wrapper.cache_clear = lambda: cache.clear()
        wrapper.cache_info = lambda: {
            "size": len(cache),
            "max_size": max_size,
            "ttl": ttl_seconds,
        }

        return wrapper

    return decorator


def validate_permissions(required_permissions: list[str]) -> Callable:
    """Decorator to validate user permissions"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract current_user from kwargs (common pattern in FastAPI)
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )

            # Check if user has required permissions
            user_permissions = getattr(current_user, "permissions", [])
            missing_permissions = [
                p for p in required_permissions if p not in user_permissions
            ]

            if missing_permissions:
                logger.warning(
                    f"User {current_user.id} missing permissions: {missing_permissions}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Missing required permissions: {', '.join(missing_permissions)}",
                )

            logger.debug(
                f"User {current_user.id} has required permissions: {required_permissions}"
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator


def rate_limit(max_calls: int = 10, time_window: int = 60) -> Callable:
    """Decorator to implement rate limiting"""

    def decorator(func: Callable) -> Callable:
        call_records: Dict[str, list[float]] = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract user identifier for rate limiting
            current_user = kwargs.get("current_user")
            if not current_user:
                # Fallback to IP-based limiting (would need request object)
                user_id = "anonymous"
            else:
                user_id = str(current_user.id)

            current_time = time.time()

            # Initialize user record if not exists
            if user_id not in call_records:
                call_records[user_id] = []

            # Clean old records outside time window
            call_records[user_id] = [
                call_time
                for call_time in call_records[user_id]
                if current_time - call_time < time_window
            ]

            # Check rate limit
            if len(call_records[user_id]) >= max_calls:
                logger.warning(f"Rate limit exceeded for user {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Max {max_calls} calls per {time_window} seconds.",
                )

            # Record this call
            call_records[user_id].append(current_time)

            return func(*args, **kwargs)

        return wrapper

    return decorator


def database_transaction(rollback_on_error: bool = True) -> Callable:
    """Decorator to handle database transactions"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract database session from kwargs
            db: Optional[Session] = kwargs.get("db")
            if not db:
                # If no db session, just execute function
                return func(*args, **kwargs)

            try:
                result = func(*args, **kwargs)
                db.commit()
                logger.debug(f"Database transaction committed for {func.__name__}")
                return result
            except Exception as e:
                if rollback_on_error:
                    db.rollback()
                    logger.warning(
                        f"Database transaction rolled back for {func.__name__}: {str(e)}"
                    )
                else:
                    logger.error(
                        f"Database transaction failed for {func.__name__}: {str(e)}"
                    )
                raise

        return wrapper

    return decorator


def retry_on_failure(
    max_retries: int = 3, delay_seconds: float = 1.0, backoff_factor: float = 2.0
) -> Callable:
    """Decorator to retry function on failure with exponential backoff"""

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def async_wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = delay_seconds * (backoff_factor**attempt)
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay}s: {str(e)}"
                        )
                        await asyncio.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {str(e)}"
                        )

            raise last_exception

        @functools.wraps(func)
        def sync_wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        delay = delay_seconds * (backoff_factor**attempt)
                        logger.warning(
                            f"Attempt {attempt + 1} failed for {func.__name__}, retrying in {delay}s: {str(e)}"
                        )
                        time.sleep(delay)
                    else:
                        logger.error(
                            f"All {max_retries + 1} attempts failed for {func.__name__}: {str(e)}"
                        )

            raise last_exception

        # Return appropriate wrapper based on whether function is async
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


# Import asyncio for async detection
import asyncio
