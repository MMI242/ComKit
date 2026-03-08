from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from PIL import Image
import os
import uuid
import shutil
from pathlib import Path

from database import get_db
from models import Item, Request, User, ItemType, ItemStatus, RequestStatus
from schemas import UserItemResponse, ItemCreate, ItemUpdate
from auth import get_current_user

router = APIRouter(prefix="/user/items", tags=["User Items"])

MEDIA_DIR = Path(__file__).parent / "media" / "items"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

@router.get("")
def get_user_items(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items = db.query(Item).filter(Item.owner_id == current_user.id).order_by(Item.created_at.desc()).all()
    
    def make_absolute_url(url):
        if url and not url.startswith('http'):
            return f"http://localhost:8000{url}"
        return url
    
    items_list = [
        UserItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            qty=item.qty,
            remaining_qty=item.remaining_qty,
            unit=item.unit,
            thumbnail_url=make_absolute_url(item.thumbnail_url),
            photo_url=make_absolute_url(item.photo_url),
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
    name: str = Form(...),
    description: str = Form(...),
    qty: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        print(f"Creating item for user {current_user.username}: {name}")
        
        # Validate inputs
        if qty <= 0:
            raise HTTPException(status_code=400, detail="Quantity must be greater than 0")
        
        if type not in ["borrow", "share"]:
            raise HTTPException(status_code=400, detail="Type must be 'borrow' or 'share'")
            
        if status not in ["available", "borrowed"]:
            raise HTTPException(status_code=400, detail="Status must be 'available' or 'borrowed'")
        
        # Handle file upload
        photo_url = None
        thumbnail_url = None
        
        if photo:
            try:
                print(f"Photo upload received: {photo.filename}")
                
                # Simple file save for testing
                file_extension = ".jpg"
                if photo.filename:
                    file_extension = os.path.splitext(photo.filename)[1]
                
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                photo_path = os.path.join(str(MEDIA_DIR), unique_filename)
                
                print(f"Saving to: {photo_path}")
                
                # Save file
                with open(photo_path, "wb") as f:
                    f.write(photo.file.read())
                
                photo_url = f"http://localhost:8000/media/items/{unique_filename}"
                thumbnail_url = photo_url  # Same for now
                
                print(f"Photo saved successfully: {photo_url}")
                
            except Exception as e:
                print(f"Photo upload error: {e}")
                # Continue without photo instead of failing
                photo_url = None
                thumbnail_url = None
        
        print(f"Creating item in database...")
        
        # Create item
        new_item = Item(
            name=name,
            description=description,
            qty=qty,
            remaining_qty=qty,
            unit=unit,
            type=ItemType(type),
            status=ItemStatus(status),
            photo_url=photo_url,
            thumbnail_url=thumbnail_url,
            owner_id=current_user.id
        )
        
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        
        print(f"Item created successfully with ID: {new_item.id}")
        
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
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        print(f"Unexpected error creating item: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{item_id}", response_model=UserItemResponse)
def update_item(
    item_id: int,
    name: str = Form(...),
    description: str = Form(...),
    qty: int = Form(...),
    unit: str = Form(...),
    type: str = Form(...),
    status: str = Form(...),
    photo: Optional[UploadFile] = File(None),
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
    reserved_requests = db.query(Request).filter(
        Request.item_id == item_id,
        Request.status.in_([RequestStatus.PENDING, RequestStatus.APPROVED])
    ).with_entities(Request.requested_qty).all()
    
    total_reserved = sum([r[0] for r in reserved_requests])
    
    if qty < total_reserved:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reduce quantity below reserved amount ({total_reserved} already reserved)"
        )
    
    # Handle file upload
    photo_url = item.photo_url  # Keep existing if no new upload
    thumbnail_url = item.thumbnail_url  # Keep existing if no new upload
    
    if photo:
        print(f"Processing photo upload for item {item_id}: {photo.filename}")
        
        # Validate file type
        if not photo.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Photo must be an image file")
        
        # Generate unique filename
        file_extension = os.path.splitext(photo.filename)[1] if photo.filename else '.jpg'
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        photo_path = MEDIA_DIR / unique_filename
        
        print(f"Saving photo to: {photo_path}")
        
        # Save file
        try:
            print(f"About to save photo for item {item_id}")
            print(f"Photo object: {photo}")
            print(f"Photo filename: {photo.filename}")
            print(f"Photo content_type: {photo.content_type}")
            print(f"MEDIA_DIR: {MEDIA_DIR}")
            print(f"MEDIA_DIR exists: {MEDIA_DIR.exists()}")
            print(f"Target path: {photo_path}")
            
            # Ensure directory exists
            MEDIA_DIR.mkdir(parents=True, exist_ok=True)
            print(f"Directory created/verified")
            
            # Try to read file content
            file_content = photo.file.read()
            print(f"Read {len(file_content)} bytes from upload")
            
            # Reset file pointer for writing
            photo.file.seek(0)
            print(f"Reset file pointer")
            
            with open(photo_path, "wb") as buffer:
                print(f"Opened file for writing")
                shutil.copyfileobj(photo.file, buffer)
                print(f"File copy completed")
                
            # Verify file was created
            if photo_path.exists():
                size = photo_path.stat().st_size
                print(f"File created successfully, size: {size} bytes")
            else:
                print(f"File was NOT created!")
                
            photo_url = f"/media/items/{unique_filename}"
            print(f"Photo URL set: {photo_url}")
        except Exception as e:
            print(f"Error in photo saving: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail="Failed to save photo file")
        
        # Create thumbnail
        try:
            img = Image.open(photo_path)
            img.thumbnail((300, 300))
            thumbnail_filename = f"{uuid.uuid4()}_thumb{file_extension}"
            thumbnail_path = MEDIA_DIR / thumbnail_filename
            img.save(thumbnail_path)
            thumbnail_url = f"/media/items/{thumbnail_filename}"
            print(f"Thumbnail created: {thumbnail_url}")
        except Exception as e:
            print(f"Failed to create thumbnail (continuing without): {e}")
            # Continue without thumbnail
    
    # Update item
    item.name = name
    item.description = description
    item.qty = qty
    item.remaining_qty = qty - total_reserved
    item.unit = unit
    item.type = ItemType(type)
    item.status = ItemStatus(status)
    item.photo_url = photo_url
    item.thumbnail_url = thumbnail_url
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
