from datetime import datetime, timedelta
from typing import Optional

from fastapi.exceptions import HTTPException
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from pydantic.networks import EmailStr
from jose import JWTError, jwt
from passlib.context import CryptContext

from app import schemas
from . import constants
from .. import crud, database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def user_pwd_hash(password: str):
    return pwd_context.hash(password)
    
def verify_user_password(password_attempt, hashed_password):
    return pwd_context.verify(password_attempt, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, constants.SECRET_KEY, algorithm=constants.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token,  constants.SECRET_KEY, [constants.ALGORITHM])
        token_id: str = payload.get("user_id")
        token_email: EmailStr = payload.get("user_email")

        if token_id is None or token_email is None:
            raise credential_exception

        token_data = schemas.TokenData(id=token_id, email=token_email)

    except JWTError as e:
        raise credential_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could Not Validate Credentials", headers={"WWW-Authenticate": "Bearer"})

    token_data = verify_access_token(token, credentials_exception)
    user = crud.get_user(db=db, user_id=token_data.id)

    if user is None:
        raise credentials_exception

    return user

    