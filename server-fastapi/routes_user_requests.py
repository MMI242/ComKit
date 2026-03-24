from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Request, Item, User, RequestStatus
from schemas import RequestListResponse, RequestResponse, RequestItemInfo, RequestUser, RequestStatusUpdate
from auth import get_current_user
from notifications import notification_manager, create_request_notification
import os

router = APIRouter(prefix="/user/requests", tags=["User Requests"])

# Check if notifications are enabled
ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "true").lower() == "true"

@router.get("", response_model=RequestListResponse)
def get_user_requests(
    type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if type not in ["incoming", "outgoing"]:
        raise HTTPException(status_code=400, detail="Type must be 'incoming' or 'outgoing'")
    
    if type == "incoming":
        # Requests to items I own
        requests = db.query(Request).join(Item).filter(
            Item.owner_id == current_user.id
        ).order_by(Request.created_at.desc()).all()
        
        response_list = []
        for req in requests:
            requester = db.query(User).filter(User.id == req.requester_id).first()
            response_list.append(RequestResponse(
                id=req.id,
                item=RequestItemInfo(
                    id=req.item.id,
                    name=req.item.name,
                    unit=req.item.unit,
                    thumbnail_url=req.item.thumbnail_url
                ),
                requester=RequestUser(
                    id=requester.id,
                    username=requester.username,
                    name=requester.name,
                    address=requester.address
                ),
                owner=None,
                requested_qty=req.requested_qty,
                unit=req.item.unit,
                date_start=req.date_start,
                date_end=req.date_end,
                status=req.status.value,
                created_at=req.created_at,
                updated_at=req.updated_at
            ))
    else:
        # Requests I made
        requests = db.query(Request).filter(
            Request.requester_id == current_user.id
        ).order_by(Request.created_at.desc()).all()
        
        response_list = []
        for req in requests:
            owner = db.query(User).filter(User.id == req.item.owner_id).first()
            response_list.append(RequestResponse(
                id=req.id,
                item=RequestItemInfo(
                    id=req.item.id,
                    name=req.item.name,
                    unit=req.item.unit,
                    thumbnail_url=req.item.thumbnail_url
                ),
                requester=None,
                owner=RequestUser(
                    id=owner.id,
                    username=owner.username,
                    name=owner.name,
                    address=owner.address
                ),
                requested_qty=req.requested_qty,
                unit=req.item.unit,
                date_start=req.date_start,
                date_end=req.date_end,
                status=req.status.value,
                created_at=req.created_at,
                updated_at=req.updated_at
            ))
    
    return RequestListResponse(requests=response_list)

@router.patch("/{request_id}", response_model=RequestResponse)
async def update_request_status(
    request_id: int,
    status_update: RequestStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Get request
    request = db.query(Request).filter(Request.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    item = db.query(Item).filter(Item.id == request.item_id).first()
    
    # Check authorization and valid transitions
    new_status = status_update.status
    current_status = request.status.value
    
    # Owner can: approve, reject, returned
    # Requester can: cancel
    is_owner = item.owner_id == current_user.id
    is_requester = request.requester_id == current_user.id
    
    if not (is_owner or is_requester):
        raise HTTPException(status_code=403, detail="You are not authorized to update this request")
    
    # Validate status transitions
    valid = False
    
    if current_status == "pending":
        if new_status == "approved" and is_owner:
            valid = True
        elif new_status == "rejected" and is_owner:
            valid = True
            # Return remaining_qty
            item.remaining_qty += request.requested_qty
        elif new_status == "cancelled" and is_requester:
            valid = True
            # Return remaining_qty
            item.remaining_qty += request.requested_qty
    elif current_status == "approved":
        if new_status == "returned" and is_owner:
            valid = True
            # Return remaining_qty
            item.remaining_qty += request.requested_qty
    
    if not valid:
        raise HTTPException(status_code=400, detail="Invalid status transition")
    
    # Update status
    request.status = RequestStatus(new_status)
    request.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(request)
    
    # Get requester/owner info for notifications
    requester = db.query(User).filter(User.id == request.requester_id).first()
    owner = db.query(User).filter(User.id == item.owner_id).first()
    
    # Send real-time notifications
    if ENABLE_NOTIFICATIONS:
        try:
            # Determine notification type and recipient
            if is_owner:
                # Owner action - notify requester
                notification_recipient_id = request.requester_id
                notification_type = f"request_{new_status}"
            else:
                # Requester action - notify owner
                notification_recipient_id = item.owner_id
                notification_type = f"request_{new_status}"
            
            # Create and send notification
            notification = create_request_notification(
                type=notification_type,
                request_id=request.id,
                item_name=item.name,
                requester_name=requester.name,
                owner_name=owner.name,
                status=new_status
            )
            
            await notification_manager.send_personal_notification(notification_recipient_id, notification)
            
        except Exception as e:
            # Log error but don't fail the request
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Failed to send notification: {e}")
    
    return RequestResponse(
        id=request.id,
        item=RequestItemInfo(
            id=item.id,
            name=item.name,
            unit=item.unit,
            thumbnail_url=item.thumbnail_url
        ),
        requester=RequestUser(
            id=requester.id,
            username=requester.username,
            name=requester.name
        ) if is_owner else None,
        owner=RequestUser(
            id=owner.id,
            username=owner.username,
            name=owner.name
        ) if is_requester else None,
        requested_qty=request.requested_qty,
        unit=item.unit,
        date_start=request.date_start,
        date_end=request.date_end,
        status=request.status.value,
        created_at=request.created_at,
        updated_at=request.updated_at
    )
