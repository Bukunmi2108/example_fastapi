# from typing import *
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# from fastapi.params import Body
# from pydantic import BaseModel
# # from random import randrange
# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time
from sqlalchemy.orm import Session
from . import models
from .schemas import *
from .database import engine, get_db
from .utils import *
from .routers import post, user, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# while True:
#     try:
#         conn = psycopg2.connect(
#             host = 'localhost',
#             database = 'fastapi',
#             user = 'postgres',
#             password = 'vivaslegan21',
#             cursor_factory= RealDictCursor
#         )
        
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print(f"This error was {error}")
#         time.sleep(2)

# my_posts = [
#     {
#         "title": "title of post 1",
#         "content": "content of post 1",
#         "id": 1
#     },
#     {
#         "title": "title of post 2",
#         "content": "content of post 2",
#         "id": 2
#     },
#     {
#         "title": "title of post 3",
#         "content": "content of post 3",
#         "id": 3
#     },
#     {
#         "title": "title of post 4",
#         "content": "content of post 4",
#         "id": 4
#     },
# ]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def read_root():
    return {"message": "This is my API"}




