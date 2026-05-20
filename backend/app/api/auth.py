# api/auth.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest, CreateUserRequest
from app.auth import service
from app.auth.dependencies import get_current_user, require_roles
from app.core.roles import UserRole
from app.core.security import hash_password
from app.db.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, request: Request, db: Session = Depends(get_db)):
    return service.login(body.email, body.password, db, request.client.host)

@router.post("/refresh")
def refresh(body: RefreshRequest, db: Session = Depends(get_db)):
    return service.refresh_access_token(body.refresh_token, db)

@router.post("/logout")
def logout(body: RefreshRequest, db: Session = Depends(get_db),
           current_user=Depends(get_current_user)):
    service.logout(current_user.id, body.refresh_token, db)
    return {"message": "Logged out successfully"}

@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email,
            "role": current_user.role, "full_name": current_user.full_name}

# Only super_admin can create users
@router.post("/users")
def create_user(body: CreateUserRequest, db: Session = Depends(get_db),
                _ = Depends(require_roles(UserRole.SUPER_ADMIN))):
    user = User(**body.dict(exclude={"password"}),
                hashed_password=hash_password(body.password))
    db.add(user)
    db.commit()
    return {"message": "User created", "id": user.id}