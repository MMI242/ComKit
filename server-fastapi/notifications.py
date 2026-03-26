from typing import Dict, List
from fastapi import WebSocket
import json
import logging
from abc import ABC, abstractmethod
from decorators import log_execution_time, retry_on_failure

logger = logging.getLogger(__name__)


class NotificationManager:
    """Singleton class for managing WebSocket connections and notifications"""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # Only initialize once
        if not NotificationManager._initialized:
            # Store active connections by user_id
            self.active_connections: Dict[int, List[WebSocket]] = {}
            NotificationManager._initialized = True
            logger.info("NotificationManager singleton initialized")

    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a WebSocket for a specific user"""
        await websocket.accept()

        if user_id not in self.active_connections:
            self.active_connections[user_id] = []

        self.active_connections[user_id].append(websocket)
        logger.info(
            f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}"
        )

    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a WebSocket for a specific user"""
        if user_id in self.active_connections:
            try:
                self.active_connections[user_id].remove(websocket)
                logger.info(
                    f"User {user_id} disconnected. Remaining connections: {len(self.active_connections[user_id])}"
                )

                # Clean up empty user entries
                if len(self.active_connections[user_id]) == 0:
                    del self.active_connections[user_id]
            except ValueError:
                logger.warning(f"WebSocket not found for user {user_id}")

    @log_execution_time
    @retry_on_failure(max_retries=3, delay_seconds=0.1)
    async def send_personal_notification(self, user_id: int, notification: dict):
        """Send a notification to a specific user"""
        if user_id in self.active_connections:
            disconnected_websockets = []

            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(json.dumps(notification))
                except Exception as e:
                    logger.error(f"Error sending notification to user {user_id}: {e}")
                    disconnected_websockets.append(connection)

            # Remove disconnected websockets
            for ws in disconnected_websockets:
                self.disconnect(ws, user_id)
        else:
            logger.info(f"No active connections for user {user_id}")

    @log_execution_time
    async def broadcast_notification(self, notification: dict):
        """Broadcast a notification to all connected users"""
        for user_id, connections in self.active_connections.items():
            disconnected_websockets = []

            for connection in connections:
                try:
                    await connection.send_text(json.dumps(notification))
                except Exception as e:
                    logger.error(f"Error broadcasting to user {user_id}: {e}")
                    disconnected_websockets.append(connection)

            # Remove disconnected websockets
            for ws in disconnected_websockets:
                self.disconnect(ws, user_id)

    def get_connected_users(self) -> List[int]:
        """Get list of currently connected user IDs"""
        return list(self.active_connections.keys())

    def get_user_connection_count(self, user_id: int) -> int:
        """Get number of active connections for a user"""
        return len(self.active_connections.get(user_id, []))

    def get_stats(self) -> dict:
        """Get connection statistics"""
        return {
            "total_users": len(self.active_connections),
            "total_connections": sum(
                len(connections) for connections in self.active_connections.values()
            ),
            "connected_users": list(self.active_connections.keys()),
        }


# Abstract Factory for creating notifications
class NotificationFactory(ABC):
    """Abstract base class for notification factories"""

    @abstractmethod
    def create_notification(self, **kwargs) -> dict:
        """Create a notification with given parameters"""
        pass

    def _create_base_notification(self, notification_type: str, data: dict) -> dict:
        """Create base notification structure"""
        return {
            "type": notification_type,
            "data": data,
            "timestamp": json.dumps(
                {"$date": {"$numberLong": str(int(__import__("time").time() * 1000))}}
            ),
        }


class RequestNotificationFactory(NotificationFactory):
    """Factory for creating request-related notifications"""

    def create_notification(self, **kwargs) -> dict:
        """Create a request status update notification"""
        return self._create_base_notification(
            "request_update",
            {
                "request_id": kwargs.get("request_id"),
                "item_name": kwargs.get("item_name"),
                "requester_name": kwargs.get("requester_name"),
                "owner_name": kwargs.get("owner_name"),
                "status": kwargs.get("status"),
                "notification_type": kwargs.get("notification_type"),
            },
        )


class NewRequestNotificationFactory(NotificationFactory):
    """Factory for creating new request notifications"""

    def create_notification(self, **kwargs) -> dict:
        """Create a new incoming request notification"""
        return self._create_base_notification(
            "new_request",
            {
                "request_id": kwargs.get("request_id"),
                "item_name": kwargs.get("item_name"),
                "requester_name": kwargs.get("requester_name"),
                "requested_qty": kwargs.get("requested_qty"),
                "unit": kwargs.get("unit"),
            },
        )


class NotificationFactoryProvider:
    """Provider class to manage notification factories"""

    @staticmethod
    def get_factory(notification_type: str) -> NotificationFactory:
        """Get the appropriate factory for the notification type"""
        factories = {
            "request_update": RequestNotificationFactory(),
            "new_request": NewRequestNotificationFactory(),
        }

        factory = factories.get(notification_type)
        if not factory:
            raise ValueError(f"Unknown notification type: {notification_type}")

        return factory


# Singleton instance
notification_manager = NotificationManager()


# Convenience functions for backward compatibility
def create_request_notification(
    type: str,
    request_id: int,
    item_name: str,
    requester_name: str,
    owner_name: str,
    status: str,
) -> dict:
    """Create a standardized request notification (backward compatibility)"""
    factory = NotificationFactoryProvider.get_factory("request_update")
    return factory.create_notification(
        request_id=request_id,
        item_name=item_name,
        requester_name=requester_name,
        owner_name=owner_name,
        status=status,
        notification_type=type,
    )


def create_new_request_notification(
    request_id: int, item_name: str, requester_name: str, requested_qty: int, unit: str
) -> dict:
    """Create a notification for new incoming request (backward compatibility)"""
    factory = NotificationFactoryProvider.get_factory("new_request")
    return factory.create_notification(
        request_id=request_id,
        item_name=item_name,
        requester_name=requester_name,
        requested_qty=requested_qty,
        unit=unit,
    )
