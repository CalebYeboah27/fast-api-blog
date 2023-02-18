from fastapi import Depends, FastAPI, Request
from router import blog_get, blog_post, user, article, product, file
from templates import templates
from auth import authentication
from db import models
from db.database import engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import time


app = FastAPI()
app.include_router(file.router)
app.include_router(templates.router)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(article.router)
app.include_router(product.router)
app.include_router(blog_get.router)
app.include_router(blog_post.router)


@app.get('/')
def home():
    return {'message': 'Welcome to Fast Api Practise project'}


@app.get('/hello')
def index():
    return {'message': 'Hello World!'}


models.Base.metadata.create_all(engine)


@app.middleware("http")
async def add_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers['duration'] = str(duration)
    return response

# Allow CORS

origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*']
)


# Making system files statically available to the browser without APIs
# in docker be sure to use => StaticFiles(directory='app/static')
app.mount('/files', StaticFiles(directory='/files'), name='files')
app.mount('/templates/static',
          StaticFiles(directory='templates/static'),
          name='static'
          )
