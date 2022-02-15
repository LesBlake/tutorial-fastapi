from typing import List, Optional

import models
import schemas
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from util import constants, utils

router = APIRouter(prefix="/posts", tags=["Posts"])


# *********************** Create POST API ***********************
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_object: object = Depends(utils.get_current_user),
):
    db_post = models.Post(owner_id=user_object.id, **post.dict())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


# *********************** Read POST APIs ***********************
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    user_object: object = Depends(utils.get_current_user),
    limit: Optional[int] = 10,
    skip: Optional[int] = 0,
    search: Optional[str] = "",
):

    posts_votes = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    return posts_votes


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    user_object: object = Depends(utils.get_current_user),
):

    post_votes = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)
        .group_by(models.Post.id)
        .filter(models.Post.id == id)
        .first()
    )

    if not post_votes:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"post with id: {id}, was not found"
        )
    else:
        return post_votes


# *********************** Update POST APIs ***********************
@router.put("/{id}", response_model=schemas.Post)
def update_all_posts(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_object: object = Depends(utils.get_current_user),
):

    query = db.query(models.Post).filter(models.Post.id == id)
    query_resp = query.first()

    if query_resp is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Was unable to find post: {id}, no post updated",
        )

    if query_resp.owner_id != user_object.id:
        print(
            f"{constants.BColors.FAIL}ERROR:    {constants.BColors.WARNING}You do not have permission to perform that action!"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform that action!",
        )

    query.update(post.dict(), synchronize_session=False)
    db.commit()
    db.refresh(query_resp)

    return query_resp


# *********************** Delete POST API ***********************
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_posts(
    id: int,
    db: Session = Depends(get_db),
    user_object: object = Depends(utils.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        print(
            f"{constants.BColors.FAIL}ERROR:    {constants.BColors.WARNING}Was unable to find post: {id}, no post deleted."
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Was unable to find post: {id}, no post deleted",
        )

    if post.first().owner_id != user_object.id:
        print(
            f"{constants.BColors.FAIL}ERROR:    {constants.BColors.WARNING}You do not have permission to perform that action!"
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform that action!",
        )

    post.delete(synchronize_session=False)
    db.commit()
