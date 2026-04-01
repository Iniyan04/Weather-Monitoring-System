from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, crud
import hashlib

router = APIRouter(prefix="/auth", tags=["Auth"])


# ---------------- REGISTER ----------------
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    existing_user = crud.get_user_by_username(db, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash password
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    new_user = crud.create_user(db, user.username, hashed_password)
    return new_user


# ---------------- LOGIN ----------------
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    
    db_user = crud.get_user_by_username(db, user.username)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid username")

    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()

    if db_user.password != hashed_password:
        raise HTTPException(status_code=400, detail="Invalid password")

    return {"message": "Login successful", "user_id": db_user.id}