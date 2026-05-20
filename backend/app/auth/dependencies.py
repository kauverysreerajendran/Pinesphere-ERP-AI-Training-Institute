# auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.core.roles import UserRole, ROLE_PERMISSIONS
from app.db.database import get_db
from app.models.user import User

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
) -> User:
    token = credentials.credentials
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def require_roles(*roles: UserRole):
    """Use: Depends(require_roles(UserRole.SUPER_ADMIN, UserRole.BRANCH_ADMIN))"""
    def checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access denied. Required role(s): {', '.join(roles)}"
            )
        return current_user
    return checker

def require_permission(section: str):
    """Use: Depends(require_permission('finance'))"""
    def checker(current_user: User = Depends(get_current_user)):
        allowed = ROLE_PERMISSIONS.get(current_user.role, [])
        if section not in allowed:
            raise HTTPException(status_code=403, detail=f"No permission for: {section}")
        return current_user
    return checker