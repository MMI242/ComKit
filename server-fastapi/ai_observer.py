from abc import ABC, abstractmethod
from typing import Any, Dict, List
import logging
import asyncio
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


class NotificationType(Enum):
    """Types of notifications that can be sent"""

    REQUEST_STARTED = "request_started"
    REQUEST_COMPLETED = "request_completed"
    REQUEST_FAILED = "request_failed"
    REQUEST_RETRYING = "request_retrying"
    REQUEST_FALLBACK = "request_fallback"
    REQUEST_CANCELLED = "request_cancelled"
    PROVIDER_SWITCH = "provider_switch"
    PERFORMANCE_WARNING = "performance_warning"


@dataclass
class NotificationEvent:
    """Event data structure for notifications"""

    event_type: NotificationType
    request_id: str
    user_id: int
    timestamp: datetime
    data: Dict[str, Any]
    message: str


class Observer(ABC):
    """Abstract base class for observers"""

    @abstractmethod
    async def update(self, event: NotificationEvent) -> None:
        """Handle notification event"""
        pass

    @abstractmethod
    def get_observer_id(self) -> str:
        """Get unique observer identifier"""
        pass


class Subject(ABC):
    """Abstract base class for subjects (observable objects)"""

    @abstractmethod
    def attach(self, observer: Observer) -> None:
        """Attach an observer to the subject"""
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        """Detach an observer from the subject"""
        pass

    @abstractmethod
    async def notify(self, event: NotificationEvent) -> None:
        """Notify all attached observers"""
        pass


class AIRequestNotifier(Subject):
    """Concrete subject that manages AI request notifications"""

    def __init__(self):
        self._observers: List[Observer] = []
        self._event_history: List[NotificationEvent] = []
        self._max_history = 1000

    def attach(self, observer: Observer) -> None:
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
            logger.info(f"Attached observer: {observer.get_observer_id()}")

    def detach(self, observer: Observer) -> None:
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
            logger.info(f"Detached observer: {observer.get_observer_id()}")

    async def notify(self, event: NotificationEvent) -> None:
        """Notify all observers of an event"""
        # Store event in history
        self._event_history.append(event)

        # Trim history if needed
        if len(self._event_history) > self._max_history:
            self._event_history = self._event_history[-self._max_history :]

        # Notify all observers
        tasks = []
        for observer in self._observers:
            try:
                task = asyncio.create_task(observer.update(event))
                tasks.append(task)
            except Exception as e:
                logger.error(
                    f"Error creating notification task for {observer.get_observer_id()}: {e}"
                )

        # Wait for all notifications to complete (with timeout)
        if tasks:
            try:
                await asyncio.gather(*tasks, timeout=5.0, return_exceptions=True)
            except Exception as e:
                logger.error(f"Error in notification batch: {e}")

        logger.info(
            f"Notified {len(self._observers)} observers of {event.event_type.value}"
        )

    def get_event_history(self, limit: int = 100) -> List[NotificationEvent]:
        """Get recent event history"""
        return self._event_history[-limit:]

    def get_observer_count(self) -> int:
        """Get number of attached observers"""
        return len(self._observers)


# Concrete Observer Implementations


class LoggingObserver(Observer):
    """Observer that logs events to file/console"""

    def __init__(self, log_level: str = "INFO"):
        self.observer_id = f"logging_observer_{id(self)}"
        self.log_level = log_level.upper()

    async def update(self, event: NotificationEvent) -> None:
        """Log the event"""
        log_message = f"[{event.event_type.value.upper()}] Request {event.request_id} for User {event.user_id}: {event.message}"

        if self.log_level == "DEBUG":
            log_message += f" | Data: {event.data}"

        if event.event_type in [
            NotificationType.REQUEST_FAILED,
            NotificationType.PERFORMANCE_WARNING,
        ]:
            logger.warning(log_message)
        else:
            logger.info(log_message)

    def get_observer_id(self) -> str:
        return self.observer_id


class MetricsObserver(Observer):
    """Observer that tracks performance metrics"""

    def __init__(self):
        self.observer_id = f"metrics_observer_{id(self)}"
        self.metrics = {
            "total_requests": 0,
            "completed_requests": 0,
            "failed_requests": 0,
            "retry_count": 0,
            "fallback_count": 0,
            "provider_usage": {},
            "average_duration": 0.0,
            "durations": [],
        }

    async def update(self, event: NotificationEvent) -> None:
        """Update metrics based on event"""
        if event.event_type == NotificationType.REQUEST_STARTED:
            self.metrics["total_requests"] += 1

        elif event.event_type == NotificationType.REQUEST_COMPLETED:
            self.metrics["completed_requests"] += 1
            duration = event.data.get("duration")
            if duration:
                self.metrics["durations"].append(duration)
                self.metrics["average_duration"] = sum(self.metrics["durations"]) / len(
                    self.metrics["durations"]
                )

        elif event.event_type == NotificationType.REQUEST_FAILED:
            self.metrics["failed_requests"] += 1

        elif event.event_type == NotificationType.REQUEST_RETRYING:
            self.metrics["retry_count"] += 1

        elif event.event_type == NotificationType.REQUEST_FALLBACK:
            self.metrics["fallback_count"] += 1

        elif event.event_type == NotificationType.PROVIDER_SWITCH:
            provider = event.data.get("provider", "unknown")
            self.metrics["provider_usage"][provider] = (
                self.metrics["provider_usage"].get(provider, 0) + 1
            )

        elif event.event_type == NotificationType.PERFORMANCE_WARNING:
            # Track performance issues
            logger.warning(f"Performance warning: {event.message}")

    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return self.metrics.copy()

    def get_observer_id(self) -> str:
        return self.observer_id


class WebSocketObserver(Observer):
    """Observer that sends notifications via WebSocket"""

    def __init__(self, notification_manager):
        self.observer_id = f"websocket_observer_{id(self)}"
        self.notification_manager = notification_manager

    async def update(self, event: NotificationEvent) -> None:
        """Send notification via WebSocket"""
        try:
            notification = {
                "type": "ai_request_update",
                "event_type": event.event_type.value,
                "request_id": event.request_id,
                "user_id": event.user_id,
                "message": event.message,
                "data": event.data,
                "timestamp": event.timestamp.isoformat(),
            }

            # Send to specific user
            await self.notification_manager.send_personal_notification(
                event.user_id, notification
            )

            logger.debug(f"WebSocket notification sent for request {event.request_id}")

        except Exception as e:
            logger.error(f"Failed to send WebSocket notification: {e}")

    def get_observer_id(self) -> str:
        return self.observer_id


class EmailObserver(Observer):
    """Observer that sends email notifications for important events"""

    def __init__(self, smtp_config: Dict[str, Any]):
        self.observer_id = f"email_observer_{id(self)}"
        self.smtp_config = smtp_config
        self.important_events = {
            NotificationType.REQUEST_FAILED,
            NotificationType.PERFORMANCE_WARNING,
        }

    async def update(self, event: NotificationEvent) -> None:
        """Send email for important events"""
        if event.event_type not in self.important_events:
            return

        try:
            # This would integrate with an email service
            # For now, just log the email that would be sent
            email_content = f"""
            AI Request {event.event_type.value.upper()}
            
            Request ID: {event.request_id}
            User ID: {event.user_id}
            Time: {event.timestamp}
            Message: {event.message}
            Data: {event.data}
            """

            logger.info(f"EMAIL NOTIFICATION (would send): {email_content}")

        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")

    def get_observer_id(self) -> str:
        return self.observer_id


class DatabaseObserver(Observer):
    """Observer that stores events in database"""

    def __init__(self, db_session_factory):
        self.observer_id = f"database_observer_{id(self)}"
        self.db_session_factory = db_session_factory

    async def update(self, event: NotificationEvent) -> None:
        """Store event in database"""
        try:
            # This would store in a notifications/events table
            # For now, just simulate database storage
            event_record = {
                "event_type": event.event_type.value,
                "request_id": event.request_id,
                "user_id": event.user_id,
                "timestamp": event.timestamp,
                "message": event.message,
                "data": event.data,
            }

            logger.debug(f"DATABASE EVENT (would store): {event_record}")

        except Exception as e:
            logger.error(f"Failed to store event in database: {e}")

    def get_observer_id(self) -> str:
        return self.observer_id


class EventPublisher:
    """Utility class to publish events to the notifier"""

    def __init__(self, notifier: AIRequestNotifier):
        self.notifier = notifier

    async def publish_request_started(
        self, request_id: str, user_id: int, ingredients: str
    ):
        """Publish request started event"""
        event = NotificationEvent(
            event_type=NotificationType.REQUEST_STARTED,
            request_id=request_id,
            user_id=user_id,
            timestamp=datetime.now(),
            data={"ingredients": ingredients},
            message=f"Started processing recipe request for ingredients: {ingredients[:50]}...",
        )
        await self.notifier.notify(event)

    async def publish_request_completed(
        self, request_id: str, user_id: int, result: Dict[str, Any], duration: float
    ):
        """Publish request completed event"""
        event = NotificationEvent(
            event_type=NotificationType.REQUEST_COMPLETED,
            request_id=request_id,
            user_id=user_id,
            timestamp=datetime.now(),
            data={"result": result, "duration": duration},
            message=f"Recipe request completed in {duration:.2f}s using {result.get('provider', 'unknown')}",
        )
        await self.notifier.notify(event)

    async def publish_request_failed(
        self, request_id: str, user_id: int, error: str, attempts: int
    ):
        """Publish request failed event"""
        event = NotificationEvent(
            event_type=NotificationType.REQUEST_FAILED,
            request_id=request_id,
            user_id=user_id,
            timestamp=datetime.now(),
            data={"error": error, "attempts": attempts},
            message=f"Recipe request failed after {attempts} attempts: {error}",
        )
        await self.notifier.notify(event)

    async def publish_request_retrying(
        self, request_id: str, user_id: int, attempt: int, error: str
    ):
        """Publish request retrying event"""
        event = NotificationEvent(
            event_type=NotificationType.REQUEST_RETRYING,
            request_id=request_id,
            user_id=user_id,
            timestamp=datetime.now(),
            data={"attempt": attempt, "error": error},
            message=f"Retrying recipe request (attempt {attempt}) after error: {error[:50]}...",
        )
        await self.notifier.notify(event)

    async def publish_provider_switch(
        self, request_id: str, user_id: int, from_provider: str, to_provider: str
    ):
        """Publish provider switch event"""
        event = NotificationEvent(
            event_type=NotificationType.PROVIDER_SWITCH,
            request_id=request_id,
            user_id=user_id,
            timestamp=datetime.now(),
            data={"from_provider": from_provider, "to_provider": to_provider},
            message=f"Switched AI provider from {from_provider} to {to_provider}",
        )
        await self.notifier.notify(event)

    async def publish_performance_warning(
        self, request_id: str, user_id: int, warning: str, metrics: Dict[str, Any]
    ):
        """Publish performance warning event"""
        event = NotificationEvent(
            event_type=NotificationType.PERFORMANCE_WARNING,
            request_id=request_id,
            user_id=user_id,
            timestamp=datetime.now(),
            data={"warning": warning, "metrics": metrics},
            message=f"Performance warning: {warning}",
        )
        await self.notifier.notify(event)


# Global instances
ai_request_notifier = AIRequestNotifier()
event_publisher = EventPublisher(ai_request_notifier)
