from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import (
    LoginRequest,
    RegisterRequest,
    RefreshTokenRequest,
    AuthResponse,
    UserResponse,
)
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])


class SetAuthCookiesRequest(BaseModel):
    access_token: str
    refresh_token: str
    remember_me: bool = False


@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"user_id": user.id, "username": user.username})
    refresh_token = create_refresh_token({"user_id": user.id})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite=None,
        secure=False,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite=None,
        secure=False,
    )

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=user.id, username=user.username, name=user.name, address=user.address
        ),
    )


@router.post("/register", response_model=AuthResponse, status_code=201)
def register(
    request: RegisterRequest, response: Response, db: Session = Depends(get_db)
):
    # Check if username exists
    existing_user = db.query(User).filter(User.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    # Create new user
    new_user = User(
        username=request.username,
        password_hash=hash_password(request.password),
        name=request.name,
        address=request.address,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Auto login
    access_token = create_access_token(
        {"user_id": new_user.id, "username": new_user.username}
    )
    refresh_token = create_refresh_token({"user_id": new_user.id})

    # Set cookies for auto-login
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite=None,
        secure=False,
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite=None,
        secure=False,
    )

    return AuthResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user=UserResponse(
            id=new_user.id,
            username=new_user.username,
            name=new_user.name,
            address=new_user.address,
        ),
    )


@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    payload = decode_token(request.refresh_token)
    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    access_token = create_access_token({"user_id": user_id})

    return {"access_token": access_token, "token_type": "Bearer", "expires_in": 3600}


@router.post("/clear-cookies")
def clear_auth_cookies(response: Response):
    response.delete_cookie(
        key="access_token", httponly=True, secure=False, samesite="lax"
    )
    response.delete_cookie(
        key="refresh_token", httponly=True, secure=False, samesite="lax"
    )

    return {"message": "Cookies cleared successfully"}


@router.get("/validate-cookies", response_model=AuthResponse)
def validate_cookies(request: Request):
    # Get tokens from HTTP-only cookies
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="No access token found")

    try:
        # Validate access token
        payload = decode_token(access_token)
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Get user from database
        db = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return AuthResponse(
            access_token=access_token,
            refresh_token=refresh_token or "",
            user=UserResponse(
                id=user.id, username=user.username, name=user.name, address=user.address
            ),
        )
    except Exception:
        # If access token is invalid, try refresh token
        if refresh_token:
            try:
                payload = decode_token(refresh_token)
                user_id = payload.get("user_id")

                if user_id is None:
                    raise HTTPException(status_code=401, detail="Invalid refresh token")

                # Generate new access token
                new_access_token = create_access_token({"user_id": user_id})

                # Get user from database
                db = next(get_db())
                user = db.query(User).filter(User.id == user_id).first()

                if not user:
                    raise HTTPException(status_code=401, detail="User not found")

                return AuthResponse(
                    access_token=new_access_token,
                    refresh_token=refresh_token,
                    user=UserResponse(
                        id=user.id,
                        username=user.username,
                        name=user.name,
                        address=user.address,
                    ),
                )
            except Exception:
                raise HTTPException(status_code=401, detail="Invalid tokens")
        else:
            raise HTTPException(status_code=401, detail="No valid tokens found")
