from sqlalchemy.orm import Session
import models, auth, schemas
from datetime import datetime, timedelta

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        return None;
    hashed_password = auth.hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def log_event(
    db: Session,
    user_id: int | None,
    action: str,
    status: str,
    message: str = None,
    ip_address: str = None,
    user_agent: str = None,
):
    log = AuditLog(
        user_id = user_id,
        action = action,
        status = status,
        message = message,
        ip_address = ip_address,
        user_agent = user_agent,
    )
    db.add(log)
    db.commit()
