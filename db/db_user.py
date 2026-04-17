
from fastapi import HTTPException,status
from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas import UserBase
from db.models import DbUser
from db import models



def get_all_users(db:Session):
    return db.query(DbUser).all()    

def get_user(db:Session,id:int):
    user=db.query(DbUser).filter(DbUser.user_id==id).first()
    if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with {id} not found")
    return user  

def get_user_by_username(db:Session,username:str):
    return db.query(DbUser).filter(DbUser.username == username).first()

  



   

