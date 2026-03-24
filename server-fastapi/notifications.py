from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect
from json import JSONDecodeError
import json
import logging

logger = logging.getLogger(__name__)

class NotificationManager:
    def __init__(self):
        # Store active connections by user_id
        self.active_connections: Dict[int, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Connect a WebSocket for a specific user"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        logger.info(f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")
    
    def disconnect(self, websocket: WebSocket, user_id: int):
        """Disconnect a WebSocket for a specific user"""
        if user_id in self.active_connections:
            try:
                self.active_connections[user_id].remove(websocket)
                logger.info(f"User {user_id} disconnected. Remaining connections: {len(self.active_connections[user_id])}")
                
                # Clean up empty user entries
                if len(self.active_connections[user_id]) == 0:
                    del self.active_connections[user_id]
            except ValueError:
                logger.warning(f"WebSocket not found for user {user_id}")
    
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

# Global instance
notification_manager = NotificationManager()

# Notification templates
def create_request_notification(
    type: str,
    request_id: int,
    item_name: str,
    requester_name: str,
    owner_name: str,
    status: str
) -> dict:
    """Create a standardized request notification"""
    return {
        "type": "request_update",
        "data": {
            "request_id": request_id,
            "item_name": item_name,
            "requester_name": requester_name,
            "owner_name": owner_name,
            "status": status,
            "notification_type": type
        },
        "timestamp": json.dumps({"$date": {"$numberLong": str(int(__import__('time').time() * 1000))}})
    }

def create_new_request_notification(
    request_id: int,
    item_name: str,
    requester_name: str,
    requested_qty: int,
    unit: str
) -> dict:
    """Create a notification for new incoming request"""
    return {
        "type": "new_request",
        "data": {
            "request_id": request_id,
            "item_name": item_name,
            "requester_name": requester_name,
            "requested_qty": requested_qty,
            "unit": unit
        },
        "timestamp": json.dumps({"$date": {"$numberLong": str(int(__import__('time').time() * 1000))}})
    }
