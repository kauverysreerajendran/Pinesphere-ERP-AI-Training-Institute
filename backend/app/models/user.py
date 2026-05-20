from sqlalchemy import Column, String, Boolean, Enum as SAEnum
from app.db.database import Base
from app.core.roles import UserRole
import uuid

class User(Base):
    __tablename__ = "users"

    id           = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email        = Column(String, unique=True, nullable=False, index=True)
    phone        = Column(String, unique=True, nullable=True)
    full_name    = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role         = Column(SAEnum(UserRole), nullable=False)
    branch_id    = Column(String, nullable=True)   # null = super admin
    is_active    = Column(Boolean, default=True)