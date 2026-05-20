# schemas/auth.py
from pydantic import BaseModel, EmailStr
from app.core.roles import UserRole

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: UserRole
    full_name: str

class RefreshRequest(BaseModel):
    refresh_token: str

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str

class CreateUserRequest(BaseModel):
    email: EmailStr
    phone: str | None = None
    full_name: str
    password: str
    role: UserRole
    branch_id: str | None = None