from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import oauth2
from .. import models,schemas,oauth2
from ..database import get_db


router = APIRouter(
    prefix= "/posts",
    tags = ['Posts']
    ) 


@router.get('/',  response_model = List[schemas.PostOut])
#@router.get('/')
async def get_post(db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_users), limit : int = 10, skip : int = 0, search : Optional[str] = ""):
    # Using SQL queries:
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # If we want to display only the posts belonging to that particular user
    #post_query = db.query(models.Post).filter(models.Post.owner_id == current_user.id)

    #print(search)
    #post_query = db.query(models.Post) # db -> database object, query -> passing a sql query, models.Post -> selecting the table/model, all() -> getting all the posts
    
    # posts = post_query.filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    #if .owner_id != current_user.id :
    #   raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")
    return posts #fast-api will automatically serialize it , it changes this into json.



@router.post('/', status_code= status.HTTP_201_CREATED,  response_model = schemas.Post)
def create_post(post : schemas.PostCreate, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_users)):
    ''' 
    Using array as a database :
    post_dict = post.dict() # converts the data from the Body into a python dictionary
    post_dict['id'] = randrange(0, 1000000)
    my_posts.routerend(post_dict)
    '''
    # Using SQL queries : 
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit() # saving the changes made to the database
    
    #new_post = models.Post(title = post.title, content = post.content, published =  post.published)
    # rather than doing the above, we can unpack into a dictionary of thepydantic model 'post'
    
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id,**post.dict())
    db.add(new_post) # adding the element to the database
    db.commit()
    db.refresh(new_post) # returns the post 


    return new_post



@router.get("/{id}",  response_model = schemas.PostOut )
def get_post(id :  int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_users)):
    # Using SQL queries : 
    # # post = find_post(id)
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first() 

    post =  db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first() 

    
    
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message" : f"Post with id : {id} was not found" } 
        #the above lines are simplified into this
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=  f"Post with id : {id} was not found")

    # If we want to display only the posts belonging to that particular user
    #   post = db.query(models.Post).first()
    #  if post.owner_id != current_user.id :
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")
    
    return post



@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_users)):
    # Using SQL queries : 
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    # index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id : {id} not found",)

    if post.owner_id != current_user.id: # Making sure that user can only delete their posts
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform actions")

    post_query.delete(synchronize_session = False)
    db.commit()
    # my_posts.pop(index)
    return Response(status_code= status.HTTP_204_NO_CONTENT)



@router.put("/{id}",  response_model = schemas.Post)
def update_post(id : int, post : schemas.PostCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_users)):
    # Using SQL queries : 
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    #index = find_index_post(id)

    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id : {id} not found")

    if updated_post.owner_id !=  current_user.id: # Making sure that user can only update their posts
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not authorized to perform actions")

    post_query.update(post.dict(), synchronize_session = False)

    db.commit()
    """
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    """

    return post_query.first()
    
