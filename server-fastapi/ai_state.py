from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import logging
from enum import Enum
from ai_observer import event_publisher

logger = logging.getLogger(__name__)


class AIRequestState(Enum):
    """Enumeration of possible AI request states"""

    IDLE = "idle"
    PROCESSING = "processing"
    GENERATING = "generating"
    PARSING = "parsing"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    FALLBACK = "fallback"


class AIRequestContext:
    """Context class that maintains state and user data"""

    def __init__(self, user_id: int, ingredients: str, request_id: str):
        self.user_id = user_id
        self.ingredients = ingredients
        self.request_id = request_id
        self.current_state: AIRequestState = AIRequestState.IDLE
        self.attempts = 0
        self.max_attempts = 3
        self.error_message: Optional[str] = None
        self.result: Optional[Dict[str, Any]] = None
        self.provider_used: Optional[str] = None
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.history: list[Dict[str, Any]] = []

    def add_history_entry(
        self, state: AIRequestState, message: str, data: Optional[Dict[str, Any]] = None
    ):
        """Add entry to state change history"""
        entry = {
            "timestamp": __import__("time").time(),
            "state": state.value,
            "message": message,
            "data": data or {},
        }
        self.history.append(entry)
        logger.info(f"Request {self.request_id}: {state.value} - {message}")

        # Notify observers of state change
        self._notify_observers(state, message, data)

    async def _notify_observers(
        self, state: AIRequestState, message: str, data: Optional[Dict[str, Any]] = None
    ):
        """Notify observers of state changes"""
        try:
            if state == AIRequestState.PROCESSING:
                await event_publisher.publish_request_started(
                    self.request_id, self.user_id, self.ingredients
                )
            elif state == AIRequestState.COMPLETED and self.result:
                await event_publisher.publish_request_completed(
                    self.request_id,
                    self.user_id,
                    self.result,
                    self.get_duration() or 0.0,
                )
            elif state == AIRequestState.FAILED:
                await event_publisher.publish_request_failed(
                    self.request_id,
                    self.user_id,
                    self.error_message or "Unknown error",
                    self.attempts,
                )
            elif state == AIRequestState.RETRYING:
                await event_publisher.publish_request_retrying(
                    self.request_id, self.user_id, self.attempts, message
                )
        except Exception as e:
            logger.error(f"Error notifying observers: {e}")

    def set_state(
        self,
        new_state: AIRequestState,
        message: str = "",
        data: Optional[Dict[str, Any]] = None,
    ):
        """Change state and log the transition"""
        old_state = self.current_state
        self.current_state = new_state
        self.add_history_entry(
            new_state,
            message or f"Transitioned from {old_state.value} to {new_state.value}",
            data,
        )

    def increment_attempts(self):
        """Increment attempt counter"""
        self.attempts += 1
        logger.info(
            f"Request {self.request_id}: Attempt {self.attempts}/{self.max_attempts}"
        )

    def can_retry(self) -> bool:
        """Check if request can be retried"""
        return self.attempts < self.max_attempts

    def mark_completed(self, result: Dict[str, Any], provider: str):
        """Mark request as completed"""
        self.result = result
        self.provider_used = provider
        self.end_time = __import__("time").time()
        self.set_state(
            AIRequestState.COMPLETED, f"Successfully completed using {provider}"
        )

    def mark_failed(self, error_message: str):
        """Mark request as failed"""
        self.error_message = error_message
        self.end_time = __import__("time").time()
        self.set_state(AIRequestState.FAILED, f"Request failed: {error_message}")

    def get_duration(self) -> Optional[float]:
        """Get request duration in seconds"""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def to_dict(self) -> Dict[str, Any]:
        """Convert context to dictionary for API responses"""
        return {
            "request_id": self.request_id,
            "user_id": self.user_id,
            "ingredients": self.ingredients,
            "current_state": self.current_state.value,
            "attempts": self.attempts,
            "max_attempts": self.max_attempts,
            "error_message": self.error_message,
            "provider_used": self.provider_used,
            "duration": self.get_duration(),
            "history": self.history[-10:] if self.history else [],  # Last 10 entries
        }


class AIState(ABC):
    """Abstract base class for AI request states"""

    @abstractmethod
    async def handle(self, context: AIRequestContext) -> "AIState":
        """Handle the current state and return next state"""
        pass

    @abstractmethod
    def get_state_name(self) -> AIRequestState:
        """Get the state enum value"""
        pass


class IdleState(AIState):
    """State when request is idle/not started"""

    async def handle(self, context: AIRequestContext) -> "AIState":
        context.set_state(AIRequestState.PROCESSING, "Starting request processing")
        context.start_time = __import__("time").time()
        return ProcessingState()

    def get_state_name(self) -> AIRequestState:
        return AIRequestState.IDLE


class ProcessingState(AIState):
    """State when request is being processed"""

    async def handle(self, context: AIRequestContext) -> "AIState":
        # Validate input
        if not context.ingredients or context.ingredients.strip() == "":
            context.mark_failed("Empty ingredients")
            return FailedState()

        context.set_state(AIRequestState.GENERATING, "Generating recipe using AI")
        return GeneratingState()

    def get_state_name(self) -> AIRequestState:
        return AIRequestState.PROCESSING


class GeneratingState(AIState):
    """State when AI is generating the recipe"""

    async def handle(self, context: AIRequestContext) -> "AIState":
        try:
            # Import fresh ai_proxy instance for each attempt
            from ai_proxy import ai_proxy

            result = await ai_proxy.generate_recipe(
                ingredients=context.ingredients,
                model=None,  # Let proxy decide
            )

            context.mark_completed(result, result.get("provider", "unknown"))
            return CompletedState()

        except Exception as e:
            context.increment_attempts()
            error_msg = str(e)

            if context.can_retry():
                context.set_state(
                    AIRequestState.RETRYING, f"Retrying due to: {error_msg}"
                )
                return RetryingState()
            else:
                context.set_state(
                    AIRequestState.FALLBACK, "Primary failed, trying fallback"
                )
                return FallbackState()

    def get_state_name(self) -> AIRequestState:
        return AIRequestState.GENERATING


class RetryingState(AIState):
    """State when request is being retried"""

    async def handle(self, context: AIRequestContext) -> "AIState":
        try:
            # Add delay before retry
            await __import__("asyncio").sleep(1.0 * context.attempts)

            # Import fresh ai_proxy instance for each retry
            from ai_proxy import ai_proxy

            result = await ai_proxy.generate_recipe(
                ingredients=context.ingredients, model=None
            )

            context.mark_completed(result, result.get("provider", "unknown"))
            return CompletedState()

        except Exception as e:
            context.increment_attempts()
            error_msg = str(e)

            if context.can_retry():
                context.set_state(
                    AIRequestState.RETRYING,
                    f"Retry {context.attempts} failed: {error_msg}",
                )
                return RetryingState()  # Create new RetryingState instance
            else:
                context.set_state(
                    AIRequestState.FALLBACK, "All retries failed, trying fallback"
                )
                return FallbackState()

    def get_state_name(self) -> AIRequestState:
        return AIRequestState.RETRYING


class FallbackState(AIState):
    """State when trying fallback providers"""

    async def handle(self, context: AIRequestContext) -> "AIState":
        # No fallback providers - mark as failed
        context.mark_failed("All providers failed - no template fallback available")
        return FailedState()

    def get_state_name(self) -> AIRequestState:
        return AIRequestState.FALLBACK


class CompletedState(AIState):
    """State when request completed successfully"""

    async def handle(self, context: AIRequestContext) -> "AIState":
        # Terminal state - no further transitions
        logger.info(f"Request {context.request_id} completed successfully")
        return self  # Stay in completed state

    def get_state_name(self) -> AIRequestState:
        return AIRequestState.COMPLETED


class FailedState(AIState):
    """State when request failed permanently"""

    async def handle(self, context: AIRequestContext) -> "AIState":
        # Terminal state - no further transitions
        logger.error(f"Request {context.request_id} failed permanently")
        return self  # Stay in failed state

    def get_state_name(self) -> AIRequestState:
        return AIRequestState.FAILED


class AIStateMachine:
    """State machine that manages AI request lifecycle"""

    def __init__(self):
        self.active_requests: Dict[str, AIRequestContext] = {}

    async def process_request(
        self, user_id: int, ingredients: str, request_id: str
    ) -> AIRequestContext:
        """Process a new AI request through the state machine"""

        # Create context
        context = AIRequestContext(user_id, ingredients, request_id)
        self.active_requests[request_id] = context

        # Start with fresh state for each request
        current_state = IdleState()

        # Process through state machine
        while not isinstance(current_state, (CompletedState, FailedState)):
            current_state = await current_state.handle(context)

            # Prevent infinite loops
            if len(context.history) > 20:  # Safety limit
                context.mark_failed("Too many state transitions")
                break

        # Clean up completed/failed requests after delay
        if isinstance(current_state, (CompletedState, FailedState)):
            await self._cleanup_request(request_id)

        return context

    async def _cleanup_request(self, request_id: str):
        """Clean up request after completion"""
        await __import__("asyncio").sleep(60)  # Keep for 1 minute for status checks
        self.active_requests.pop(request_id, None)
        logger.info(f"Cleaned up request {request_id}")

    def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get status of active request"""
        context = self.active_requests.get(request_id)
        return context.to_dict() if context else None

    def get_all_active_requests(self) -> Dict[str, Dict[str, Any]]:
        """Get all active requests"""
        return {
            req_id: context.to_dict()
            for req_id, context in self.active_requests.items()
        }

    def cancel_request(self, request_id: str) -> bool:
        """Cancel an active request"""
        if request_id in self.active_requests:
            context = self.active_requests[request_id]
            context.mark_failed("Request cancelled by user")
            return True
        return False


# Global state machine instance
ai_state_machine = AIStateMachine()
