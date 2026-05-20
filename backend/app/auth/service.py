# auth/service.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.models.user import User
from app.models.token import RefreshToken, AuditLog
from app.core.security import (
    verify_password, hash_password,
    create_access_token, create_refresh_token, decode_token
)
from app.core.config import settings
import uuid

def login(email: str, password: str, db: Session, ip: str):
    user = db.query(User).filter(User.email == email).first()

    # Always log the attempt
    def log(action):
        db.add(AuditLog(user_id=user.id if user else "unknown",
                        action=action, ip_address=ip))
        db.commit()

    if not user or not verify_password(password, user.hashed_password):
        log("failed_login")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is deactivated")

    access_token  = create_access_token({"sub": user.id, "role": user.role})
    refresh_token = create_refresh_token({"sub": user.id})

    # Save refresh token to DB
    db.add(RefreshToken(
        id=str(uuid.uuid4()),
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    ))
    log("login")

    return {"access_token": access_token, "refresh_token": refresh_token,
            "role": user.role, "full_name": user.full_name}

def refresh_access_token(refresh_token: str, db: Session):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token,
        RefreshToken.revoked == False
    ).first()

    if not db_token or db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token expired or revoked")

    user = db.query(User).filter(User.id == payload["sub"]).first()
    new_access_token = create_access_token({"sub": user.id, "role": user.role})
    return {"access_token": new_access_token, "token_type": "bearer"}

def logout(user_id: str, refresh_token: str, db: Session):
    db.query(RefreshToken).filter(
        RefreshToken.user_id == user_id,
        RefreshToken.token == refresh_token
    ).update({"revoked": True})
    db.add(AuditLog(user_id=user_id, action="logout"))
    db.commit()