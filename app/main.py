from fastapi import FastAPI
from . import models
# from .database import engine
from .routers import post, user, auth, vote
# from .config import settings
from fastapi.middleware.cors import CORSMiddleware

#models.Base.metadata.create_all(bind=engine)


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# my_posts = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1},  # storing the posts in an array
#         {"title" : "favourite foods", "content" : "bagels", "id" : 2 }]


# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p


# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

app.include_router(post.router) # accesses the router object of post and checks if the specified path exist
app.include_router(user.router) # accesses the router object of user and checks if the specified path exist
app.include_router(auth.router) # accesses the router object of auth and checks if the specified path exist
app.include_router(vote.router) # accesses the router object of vote and checks if the specified path exist


@app.get('/')
def root():
    return {"message" : "Hello World!"}

