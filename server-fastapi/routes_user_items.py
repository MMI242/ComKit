from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from PIL import Image
import os
import uuid

from database import get_db
from models import Item, Request, User, ItemType, ItemStatus, RequestStatus
from schemas import UserItemResponse, ItemCreate, ItemUpdate
from auth import get_current_user

router = APIRouter(prefix="/user/items", tags=["User Items"])

MEDIA_DIR = "media/items"
os.makedirs(MEDIA_DIR, exist_ok=True)

def save_image(file: UploadFile, item_id: int) -> tuple[str, str]:
    """Save image and create thumbnail"""
    ext = file.filename.split('.')[-1]
    filename = f"{item_id}_{uuid.uuid4()}.{ext}"
    filepath = os.path.join(MEDIA_DIR, filename)
    
    # Save original
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    
    # Create thumbnail
    thumb_filename = f"{item_id}_{uuid.uuid4()}_thumb.{ext}"
    thumb_filepath = os.path.join(MEDIA_DIR, thumb_filename)
    
    with Image.open(filepath) as img:
        img.thumbnail((300, 300))
        img.save(thumb_filepath)
    
    return f"/{filepath}", f"/{thumb_filepath}"

@router.get("")
def get_user_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items = db.query(Item).filter(Item.owner_id == current_user.id).order_by(Item.created_at.desc()).all()
    
    items_list = [
        UserItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            qty=item.qty,
            remaining_qty=item.remaining_qty,
            unit=item.unit,
            thumbnail_url=item.thumbnail_url,
            photo_url=item.photo_url,
            type=item.type.value,
            status=item.status.value,
            created_at=item.created_at,
            updated_at=item.updated_at
        )
        for item in items
    ]
    
    return {"items": items_list}

@router.post("", response_model=UserItemResponse, status_code=201)
def create_item(
    item_data: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validation already done by Pydantic
    
    # Create item
    new_item = Item(
        name=item_data.name,
        description=item_data.description,
        qty=item_data.qty,
        remaining_qty=item_data.qty,
        unit=item_data.unit,
        type=ItemType(item_data.type),
        status=ItemStatus(item_data.status),
        owner_id=current_user.id
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return UserItemResponse(
        id=new_item.id,
        name=new_item.name,
        description=new_item.description,
        qty=new_item.qty,
        remaining_qty=new_item.remaining_qty,
        unit=new_item.unit,
        thumbnail_url=new_item.thumbnail_url,
        photo_url=new_item.photo_url,
        type=new_item.type.value,
        status=new_item.status.value,
        created_at=new_item.created_at,
        updated_at=new_item.updated_at
    )

@router.put("/{item_id}", response_model=UserItemResponse)
def update_item(
    item_id: int,
    item_data: ItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get item
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check ownership
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this item")
    
    # Check reserved qty
    reserved_qty = db.query(Request).filter(
        Request.item_id == item_id,
        Request.status.in_([RequestStatus.PENDING, RequestStatus.APPROVED])
    ).with_entities(Request.requested_qty).all()
    
    total_reserved = sum([r[0] for r in reserved_qty])
    
    if item_data.qty < total_reserved:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reduce quantity below reserved amount ({total_reserved} already reserved)"
        )
    
    # Update item
    item.name = item_data.name
    item.description = item_data.description
    item.qty = item_data.qty
    item.remaining_qty = item_data.qty - total_reserved
    item.unit = item_data.unit
    item.type = ItemType(item_data.type)
    item.status = ItemStatus(item_data.status)
    item.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(item)
    
    return UserItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        qty=item.qty,
        remaining_qty=item.remaining_qty,
        unit=item.unit,
        thumbnail_url=item.thumbnail_url,
        photo_url=item.photo_url,
        type=item.type.value,
        status=item.status.value,
        created_at=item.created_at,
        updated_at=item.updated_at
    )

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get item
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Check ownership
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this item")
    
    # Check for active requests
    active_requests = db.query(Request).filter(
        Request.item_id == item_id,
        Request.status.in_([RequestStatus.PENDING, RequestStatus.APPROVED])
    ).count()
    
    if active_requests > 0:
        raise HTTPException(
            status_code=400,
            detail="Cannot delete item with active requests (pending or approved)"
        )
    
    # Delete photos if exist
    if item.photo_url and os.path.exists(item.photo_url.lstrip('/')):
        os.remove(item.photo_url.lstrip('/'))
    if item.thumbnail_url and os.path.exists(item.thumbnail_url.lstrip('/')):
        os.remove(item.thumbnail_url.lstrip('/'))
    
    db.delete(item)
    db.commit()
    
    return {"message": "Item deleted successfully", "item_id": item_id}
