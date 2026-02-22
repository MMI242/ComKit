from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import LoginRequest, RegisterRequest, RefreshTokenRequest, AuthResponse, UserResponse
from auth import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token = create_access_token({"user_id": user.id, "username": user.username})
    refresh_token = create_refresh_token({"user_id": user.id})
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=user.id,
            username=user.username,
            name=user.name,
            address=user.address
        )
    )

@router.post("/register", response_model=AuthResponse, status_code=201)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    # Check if username exists
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    # Create new user
    new_user = User(
        username=request.username,
        password_hash=hash_password(request.password),
        name=request.name,
        address=request.address
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Auto login
    access_token = create_access_token({"user_id": new_user.id, "username": new_user.username})
    refresh_token = create_refresh_token({"user_id": new_user.id})
    
    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=new_user.id,
            username=new_user.username,
            name=new_user.name,
            address=new_user.address
        )
    )

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    payload = decode_token(request.refresh_token)
    user_id = payload.get("user_id")
    
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    access_token = create_access_token({"user_id": user_id})
    
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": 3600
    }
