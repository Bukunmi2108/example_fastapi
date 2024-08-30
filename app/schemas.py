from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


#schemas
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(Post):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
  id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostResponse(Post):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    # votes: Vote
    # class Config:
    #     orm_mode = True
    #     from_attributes = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int