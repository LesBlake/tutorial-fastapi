import models
import schemas
from database import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from util import constants, utils

router = APIRouter(prefix="/vote", tags=["Vote"])


# *********************** vote on post ***********************
@router.post("/", status_code=status.HTTP_201_CREATED)  # , response_model=schemas.Vote)
def vote(
    vote: schemas.Vote,
    # post: schemas.Post,
    db: Session = Depends(get_db),
    user_object: object = Depends(utils.get_current_user),
):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {vote.post_id} not found.",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == user_object.id
    )

    found_vote_query = vote_query.first()

    if vote.dir == 1:
        # if vote already present for this post and this user
        if found_vote_query:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"User: {user_object.id} has already voted on {vote.post_id}",
            )
        # if vote not present, create vote
        else:
            create_vote_query = models.Vote(
                post_id=vote.post_id, user_id=user_object.id
            )
            db.add(create_vote_query)
            db.commit()
            return {"message": "successfully added vote"}

    elif vote.dir == 0:
        # if vote already found, remove

        if found_vote_query is None:
            print(
                f"{constants.BColors.FAIL}ERROR:    {constants.BColors.WARNING}Vote:{vote.post_id} not found, no vote removed."
            )
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Was unable to find post: {id}, no vote removed",
            )

        if found_vote_query.user_id != user_object.id:
            print(
                f"{constants.BColors.FAIL}ERROR:    {constants.BColors.WARNING}You do not have permission to perform that action!"
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform that action! This vote doesn't belong to you.",
            )

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "removed vote"}
