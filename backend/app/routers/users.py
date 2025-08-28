from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, database
from passlib.context import CryptContext

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#sign up
@router.post("/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session= Depends(database.get_db)):
    #Hash password
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password = hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#list users
@router.get("/", response_model=list[schemas.UserOut])
def get_users(db:Session=Depends(database.get_db)):
    return db.query(models.User).all()