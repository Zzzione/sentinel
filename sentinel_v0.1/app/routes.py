from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import auth, crud, schemas
from database import SessionLocal
from models import AuditLog
from datetime import datetime

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@router.post("/register", response_model=schemas.UserOut)
#def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
#    if crud.get_user_by_email(db, user.email):
#        raise HTTPException(status_code=400, detail="Email already registered")
#    try:
#        return crud.create_user(db, user)
#    except Exception as e:
#        print("Error in create_user:", e)
#        raise HTTPException(status_code=500, detail=str(e))

def log_event(db: Session, user_id: int | None, action: str, status: str, message: str, request: Request):
    log = AuditLog(
        user_id=user_id,
        action=action,
        status=status,
        message=message,
        ip_address=request.client.host,
        user_agent=request.headers.get("user-agent"),
        timestamp=datetime.utcnow(),
    )
    db.add(log)
    db.commit()


@router.post("/register")  # убрал response_model временно
def register(user: schemas.UserCreate, request: Request, db: Session = Depends(get_db)):
    print("Got user:", user)
    if crud.get_user_by_username(db, user.username):
        log_event(db, db_user.id, "register", "fail", f"User {user.username} failed to register", request)
        return {"ok": False, "error": "User with this username already exists"}
    if crud.get_user_by_email(db, user.email):
        log_event(db, db_user.id, "register", "fail", f"User {user.username} failed to register", request)
        return {"ok": False, "error": "User with this email already exists"}
    new_user = crud.create_user(db, user)
    log_event(db, new_user.id, "register", "success", f"User {user.username} registered", request)
    print("Created user:", new_user)
    return {"ok": True, "user_id": new_user.id}  # просто ответ для проверки

@router.post("/login")
def login(user: schemas.UserLogin, request: Request, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user:
        log_event(db, db_user.id, "login", "fail", f"User {user.username} failed to log in", request)
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not auth.verify_password(user.password, db_user.hashed_password):
        log_event(db, db_user.id, "login", "fail", f"User {user.username} failed to log in", request)
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = auth.create_access_token({"sub": db_user.username})
    log_event(db, db_user.id, "login", "success", f"User {user.username} logged in", request)
    return {"ok": True, "user_id": db_user.id, "access_token": token, "token_type": "bearer"}

