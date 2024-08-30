from typing import *
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from .. import models
from ..schemas import *
from ..database import get_db
from ..utils import *

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=201, response_model=UserResponse)
def create_users(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user.password = hash(user.password)
        
        new_user = models.User(**user.dict())
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists!!")
    return new_user

@router.get("/", response_model= List[UserResponse])
def get_user( response: Response, db: Session = Depends(get_db)):    
    users = db.query(models.User).all()
        
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Users Available")
    return users

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):    
    un_user = db.query(models.User).filter(models.User.id == id).first()
        
    if not un_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return un_user