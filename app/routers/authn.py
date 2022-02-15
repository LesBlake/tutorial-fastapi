from app import crud, schemas
from app.database import get_db
from app.util import constants, utils
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

# from pydantic import utils
from sqlalchemy.orm import Session

# from app.util import constants
# from ..database import get_db
# from .. import schemas
# from .. import crud
# from ..util import utils


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    db_user = crud.get_user_by_email(db, email=user_credentials.username)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    if not utils.verify_user_password(user_credentials.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )

    user_dict = {"user_id": db_user.id, "user_email": db_user.email}

    # reate JWT Token
    jwt_token = utils.create_access_token(
        user_dict, constants.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    # return JWT Token
    return {"access_token": jwt_token, "token_type": "Bearer"}
