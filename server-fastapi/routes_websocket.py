from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import json
import logging

from database import get_db
from auth import get_current_user_websocket
from notifications import notification_manager
from models import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ws", tags=["websocket"])

@router.websocket("/notifications/{user_id}")
async def websocket_notifications(
    websocket: WebSocket, 
    user_id: int,
    db: Session = Depends(get_db)
):
    """WebSocket endpoint for real-time notifications"""
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        await websocket.close(code=4004, reason="User not found")
        return
    
    try:
        await notification_manager.connect(websocket, user_id)
        
        # Send welcome message
        welcome_msg = {
            "type": "connection_established",
            "data": {
                "user_id": user_id,
                "message": "Connected to notification service"
            }
        }
        await websocket.send_text(json.dumps(welcome_msg))
        
        # Keep connection alive and handle incoming messages
        while True:
            try:
                # Wait for messages (ping/pong or other client messages)
                data = await websocket.receive_text()
                
                # Parse client message
                try:
                    message = json.loads(data)
                    
                    # Handle ping messages for keepalive
                    if message.get("type") == "ping":
                        pong_response = {"type": "pong", "timestamp": message.get("timestamp")}
                        await websocket.send_text(json.dumps(pong_response))
                    
                    # Handle other client messages as needed
                    elif message.get("type") == "mark_read":
                        # Could implement notification read status here
                        logger.info(f"User {user_id} marked notification as read")
                        
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON received from user {user_id}: {data}")
                    continue
                    
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected for user {user_id}")
                break
            except Exception as e:
                logger.error(f"Error in WebSocket for user {user_id}: {e}")
                break
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for user {user_id}")
    except Exception as e:
        logger.error(f"WebSocket error for user {user_id}: {e}")
    finally:
        notification_manager.disconnect(websocket, user_id)

@router.get("/status")
async def get_websocket_status():
    """Get WebSocket connection status (for monitoring)"""
    connected_users = notification_manager.get_connected_users()
    total_connections = sum(
        notification_manager.get_user_connection_count(user_id) 
        for user_id in connected_users
    )
    
    return {
        "connected_users": len(connected_users),
        "total_connections": total_connections,
        "active_user_ids": connected_users
    }
