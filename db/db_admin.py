from sqlalchemy.orm import Session
from db.models import DbUser
from db.hash import Hash
ADMIN_ROLE_ID = 1

def seed_admin_user(db: Session):
    # Check if admin already exists
    admin = (
        db.query(DbUser)
        .filter(DbUser.sr_id == 1)
        .first()
    )

    if not admin:
        admin = DbUser(
            username="admin",
            password=Hash.bcrypt("admin123"),
            sr_id=ADMIN_ROLE_ID,
            is_active="NO"
        )
        db.add(admin)
        db.commit()
