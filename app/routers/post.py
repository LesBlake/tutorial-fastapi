
from fastapi import status, HTTPException, Depends, APIRouter
from pydantic import utils
from sqlalchemy.orm import Session

from typing import List, Optional

from .. import schemas
from .. import models
from ..database import get_db
from ..util import constants, utils


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

# *********************** Create POST API ***********************
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), user_object: object = Depends(utils.get_current_user)):
    db_post = models.Post(owner_id=user_object.id, **post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# *********************** Read POST APIs ***********************
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db), user_object: object = Depends(utils.get_current_user), limit: Optional[int] = 10, skip: Optional[int] = 0, search: Optional[str] = ''):

    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    #if limit == 0 and skip == 0:
    #    posts = db.query(models.Post).all() 
    #elif limit > 0 and skip == 0:
    #    posts = db.query(models.Post).limit(limit).all()
    #elif limit > 0 and skip > 0:
   #     posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #elif limit == 0 and skip > 0:
    #    posts = db.query(models.Post).offset(skip).all()
    
    return posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), user_object: object = Depends(utils.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id: {id}, was not found")
    else:
        return post

# *********************** Update POST APIs ***********************
@router.put("/{id}", response_model=schemas.Post)
def update_all_posts(id: int, post:schemas.PostCreate, db: Session = Depends(get_db), user_object: object = Depends(utils.get_current_user)):
    
    query = db.query(models.Post).filter(models.Post.id == id)
    query_resp = query.first()

    if query_resp == None:  
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Was unable to find post: {id}, no post updated")

    if query_resp.owner_id != user_object.id:
        print(f"{constants.BColors.FAIL}ERROR:    {constants.BColors.WARNING}You do not have permission to perform that action!")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You do not have permission to perform that action!")

    query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(query_resp)

    return query_resp

# *********************** Delete POST API ***********************
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(id: int, db: Session = Depends(get_db), user_object: object = Depends(utils.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        print(f"{constants.BColors.FAIL}ERROR:    {constants.BColors.WARNING}Was unable to find post: {id}, no post deleted.")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Was unable to find post: {id}, no post deleted")

    if post.first().owner_id != user_object.id:
        print(f"{constants.BColors.FAIL}ERROR:    {constants.BColors.WARNING}You do not have permission to perform that action!")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You do not have permission to perform that action!")

    post.delete(synchronize_session=False)
    db.commit()