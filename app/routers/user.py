from typing import List

# import models
from app import crud, schemas
from app.database import get_db
from app.util import utils  # , constants
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/users", tags=["Users"])


# *********************** Create USER API ***********************
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # hash the password from user.password
    user.password = utils.user_pwd_hash(user.password)
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


# *********************** Get USER APIs ***********************
@router.get("/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db=db)
    return users


@router.get("/{id}", response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db=db, user_id=id)
    if not user:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"user with id: {id}, was not found"
        )
    return user
