from typing import *
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models
from ..schemas import Post, Vote, PostCreate, PostResponse, PostOut
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix= "/posts",
    tags=['Posts']
)

# @router.get("/", response_model= List[PostResponse])
@router.get("/", response_model= List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):
    
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        
        # cursor.execute(
    #     """
    #     SELECT * FROM posts;
    #     """
    # )
    # posts = cursor.fetchall()
    return results

@router.post("/", status_code=201, response_model= PostCreate)
def create_posts(post: Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    
    # new_post = cursor.fetchone()
    # conn.commit()
    # To unpack a dictionary put **in front of a dictionary object
    print(current_user)
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    # un_post = db.query(models.Post).filter(models.Post.id == id).first()
    
    un_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
            
    if not un_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return un_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id),))
    
    del_post_query = db.query(models.Post).filter(models.Post.id == id)
    
    del_post = del_post_query.first()
    # conn.commit()
    if del_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    if del_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    
    del_post_query.delete(synchronize_session=False)
    db.commit()
    
    return{"message": "post was sucessfully deleted"}

@router.put("/{id}", response_model=PostResponse)
def update_post(id: int, post: Post, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE id = %s RETURNING *""", (post.title, post.content, str(id)))
    
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    
    updated = updated_post.first()
    
    if updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} does not exist")
    
    if updated.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorised to perform requested action")
    
    updated_post.update(post.dict(), synchronize_session=False)
    
    db.commit()
    
    return updated_post.first()