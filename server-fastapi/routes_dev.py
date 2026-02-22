from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from database import get_db
from models import Item, User, Request
from auth import get_current_user

load_dotenv()

router = APIRouter(prefix="/dev", tags=["Development"])

def check_dev_environment():
    """Check if we're in development environment"""
    env = os.getenv("ENVIRONMENT", "production")
    if env != "development":
        raise HTTPException(status_code=404, detail="Not found")

@router.delete("/delete/item/{item_id}")
def delete_item_dev(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_dev_environment()
    
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Delete associated photos
    if item.photo_url and os.path.exists(item.photo_url.lstrip('/')):
        os.remove(item.photo_url.lstrip('/'))
    if item.thumbnail_url and os.path.exists(item.thumbnail_url.lstrip('/')):
        os.remove(item.thumbnail_url.lstrip('/'))
    
    # Cascade delete will handle requests
    db.delete(item)
    db.commit()
    
    return {"message": "Item deleted successfully", "item_id": item_id}

@router.delete("/delete/user/{username}")
def delete_user_dev(
    username: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    check_dev_environment()
    
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Count items and requests before deletion
    items_count = db.query(Item).filter(Item.owner_id == user.id).count()
    requests_count = db.query(Request).filter(Request.requester_id == user.id).count()
    
    # Delete all user's item photos
    items = db.query(Item).filter(Item.owner_id == user.id).all()
    for item in items:
        if item.photo_url and os.path.exists(item.photo_url.lstrip('/')):
            os.remove(item.photo_url.lstrip('/'))
        if item.thumbnail_url and os.path.exists(item.thumbnail_url.lstrip('/')):
            os.remove(item.thumbnail_url.lstrip('/'))
    
    # Cascade delete will handle items and requests
    db.delete(user)
    db.commit()
    
    return {
        "message": "User and all related data deleted successfully",
        "username": username,
        "deleted_items": items_count,
        "deleted_requests": requests_count
    }
