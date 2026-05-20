import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password
from app.core.roles import UserRole
import uuid

db = SessionLocal()

existing = db.query(User).filter(User.email == "admin@pinesphere.com").first()
if existing:
    print("⚠️ Super admin already exists!")
else:
    admin = User(
        id=str(uuid.uuid4()),
        full_name="Super Admin",
        email="admin@pinesphere.com",
        hashed_password=hash_password("Admin@123"),
        role=UserRole.SUPER_ADMIN,
        is_active=True
    )
    db.add(admin)
    db.commit()
    print("✅ Super admin created!")

db.close()