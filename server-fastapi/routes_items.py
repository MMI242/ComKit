from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, date
from database import get_db
from models import Item, Request, User, RequestStatus
from schemas import ItemListResponse, ItemResponse, ItemOwner, RequestCreate, RequestResponse, RequestItemInfo, RequestUser
from auth import get_current_user

router = APIRouter(prefix="/items", tags=["Items"])

@router.get("", response_model=ItemListResponse)
def get_items(
    page: int = 1,
    search: str = "",
    type: str = "all",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    items_per_page = 25
    skip = (page - 1) * items_per_page
    
    # Build query
    query = db.query(Item)
    
    # Filter by type
    if type in ["borrow", "share"]:
        query = query.filter(Item.type == type)
    
    # Search filter
    if search:
        search_filter = or_(
            Item.name.ilike(f"%{search}%"),
            Item.description.ilike(f"%{search}%"),
            User.name.ilike(f"%{search}%")
        )
        query = query.join(User).filter(search_filter)
    
    # Get total count
    total_items = query.count()
    
    # Pagination
    items = query.offset(skip).limit(items_per_page).all()
    
    # Format response
    items_response = []
    for item in items:
        owner = db.query(User).filter(User.id == item.owner_id).first()
        items_response.append(ItemResponse(
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
            owner=ItemOwner(
                id=owner.id,
                username=owner.username,
                name=owner.name,
                address=owner.address
            )
        ))
    
    return ItemListResponse(
        items=items_response,
        pagination={
            "current_page": page,
            "total_pages": (total_items + items_per_page - 1) // items_per_page,
            "total_items": total_items,
            "items_per_page": items_per_page
        }
    )

@router.post("/{item_id}/request", status_code=201)
def request_item(
    item_id: int,
    request_data: RequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get item
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Validate quantity
    if request_data.requested_qty <= 0:
        raise HTTPException(status_code=400, detail="Requested quantity must be greater than 0")
    
    if request_data.requested_qty > item.remaining_qty:
        raise HTTPException(status_code=400, detail=f"Insufficient quantity. Only {item.remaining_qty} available")
    
    # Validate item status
    if item.status.value != "available":
        raise HTTPException(status_code=400, detail="Item is not available")
    
    # Validate dates
    try:
        start_date = datetime.strptime(request_data.date_start, "%Y-%m-%d").date()
        end_date = datetime.strptime(request_data.date_end, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
    
    if end_date < start_date:
        raise HTTPException(status_code=400, detail="End date must be after start date")
    
    if start_date < date.today():
        raise HTTPException(status_code=400, detail="Start date cannot be in the past")
    
    # Create request
    new_request = Request(
        item_id=item_id,
        requester_id=current_user.id,
        requested_qty=request_data.requested_qty,
        date_start=request_data.date_start,
        date_end=request_data.date_end,
        status=RequestStatus.PENDING
    )
    
    # Update remaining_qty (reserve)
    item.remaining_qty -= request_data.requested_qty
    
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    
    response_data = {
        "request_id": new_request.id,
        "id": new_request.id,
        "item": {
            "id": item.id,
            "name": item.name,
            "unit": item.unit
        },
        "requester": {
            "id": current_user.id,
            "username": current_user.username,
            "name": current_user.name
        },
        "requested_qty": new_request.requested_qty,
        "unit": item.unit,
        "date_start": new_request.date_start,
        "date_end": new_request.date_end,
        "status": new_request.status.value,
        "created_at": new_request.created_at,
        "updated_at": new_request.updated_at
    }
    
    return response_data
