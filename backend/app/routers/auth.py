from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from app.config import settings

router =APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated ="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password ,hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire =datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

@router.post("/login")
def login(user: schemas.UserLogin, db: Session =Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token =create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type" :"bearer"}