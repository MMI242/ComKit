from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime
import re

# Auth Schemas
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    name: str
    address: str
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-z0-9_]+$', v):
            raise ValueError('Username must be lowercase, and contain only letters, numbers, and underscores')
        return v

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: int
    username: str
    name: str
    address: str

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int = 3600
    user: UserResponse

# Item Schemas
class ItemOwner(BaseModel):
    id: int
    username: str
    name: str
    address: str

class ItemBase(BaseModel):
    id: int
    name: str
    description: str
    qty: int
    remaining_qty: int
    unit: str
    thumbnail_url: Optional[str]
    photo_url: Optional[str]
    type: str
    status: str

class ItemResponse(ItemBase):
    owner: ItemOwner

class ItemCreate(BaseModel):
    name: str
    description: str
    qty: int = Field(..., gt=0)
    unit: str = "pcs"
    type: str
    status: str = "available"
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['borrow', 'share']:
            raise ValueError("Type must be 'borrow' or 'share'")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ['available', 'borrowed']:
            raise ValueError("Status must be 'available' or 'borrowed'")
        return v

class ItemUpdate(BaseModel):
    name: str
    description: str
    qty: int = Field(..., gt=0)
    unit: str
    type: str
    status: str
    
    @validator('type')
    def validate_type(cls, v):
        if v not in ['borrow', 'share']:
            raise ValueError("Type must be 'borrow' or 'share'")
        return v
    
    @validator('status')
    def validate_status(cls, v):
        if v not in ['available', 'borrowed']:
            raise ValueError("Status must be 'available' or 'borrowed'")
        return v

class ItemListResponse(BaseModel):
    items: list[ItemResponse]
    pagination: dict

class UserItemResponse(BaseModel):
    id: int
    name: str
    description: str
    qty: int
    remaining_qty: int
    unit: str
    thumbnail_url: Optional[str]
    photo_url: Optional[str]
    type: str
    status: str
    created_at: datetime
    updated_at: datetime

# Request Schemas
class RequestCreate(BaseModel):
    requested_qty: int = Field(..., gt=0)
    date_start: str
    date_end: str

class RequestItemInfo(BaseModel):
    id: int
    name: str
    unit: str
    thumbnail_url: Optional[str] = None

class RequestUser(BaseModel):
    id: int
    username: str
    name: str
    address: Optional[str] = None

class RequestResponse(BaseModel):
    id: int
    item: RequestItemInfo
    requester: Optional[RequestUser] = None
    owner: Optional[RequestUser] = None
    requested_qty: int
    unit: str
    date_start: str
    date_end: str
    status: str
    created_at: datetime
    updated_at: datetime

class RequestStatusUpdate(BaseModel):
    status: str

class RequestListResponse(BaseModel):
    requests: list[RequestResponse]

# AI Recipe Schemas
class RecipeRequest(BaseModel):
    ingredients: str

class RecipeResponse(BaseModel):
    recipe: dict
    generated_at: datetime
    model: str  # Add model field to track which model was used
