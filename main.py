from fastapi import Depends, FastAPI
from router import blog_get, blog_post, user
from db import models
from db.database import engine, get_db


app = FastAPI()
app.include_router(user.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get('/')
def home():
    return {'message': 'Welcome to Fast Api Practise project'}


@app.get('/hello')
def index():
    return {'message': 'Hello World!'}


models.Base.metadata.create_all(engine)