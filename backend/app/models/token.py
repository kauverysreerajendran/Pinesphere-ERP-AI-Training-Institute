from sqlalchemy import Column, String, Boolean, DateTime
from app.db.database import Base
from datetime import datetime
import uuid

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id    = Column(String, nullable=False)
    token      = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    revoked    = Column(Boolean, default=False)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id    = Column(String, nullable=False)
    action     = Column(String, nullable=False)   # "login", "logout", "failed_login"
    ip_address = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)