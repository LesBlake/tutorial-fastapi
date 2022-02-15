from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, conint

# *********************** Pydantic models/schema for API verificaiton ***********************


# *********************** SCHEMA FOR USER ***********************
# ****** Base Schemas ******
class UserBase(BaseModel):
    email: EmailStr


# ****** Request Schemas ******
class UserCreate(UserBase):
    password: str


# ****** Response Schemas ******
class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(UserCreate):
    pass


# *********************** SCHEMA FOR POST ***********************
# ****** Base Schemas ******
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# ****** Request Schemas ******
class PostCreate(PostBase):
    pass


# ****** Response Schemas ******
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: User

    class Config:
        orm_mode = True


# ****** Response Schemas with Votes Join ******
class PostOut(BaseModel):
    Post: Post
    votes: int


# *********************** TOKEN SCHEMA ***********************
# ****** Base Schemas ******
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None


# *********************** SCHEMA FOR VOTE ***********************
# ****** Base Schemas ******
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
