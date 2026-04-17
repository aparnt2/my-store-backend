
from typing import List
from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session
from schemas import UserBase,UserDisplay
from db.database import get_db
from db import db_user

from auth.token_utils import oauth2_schema,get_current_user
# from auth.token_utils import get_current_user

router = APIRouter(
     prefix='/user',
     tags=['user']
)




@router.get("/",response_model=List[UserDisplay])
def get_all_users(db:Session = Depends(get_db),current_user:UserBase = Depends(get_current_user)):
    return db_user.get_all_users(db)

@router.get("/{id}",response_model=UserDisplay)  
def get_user(id:int,db:Session=Depends(get_db),current_user:UserBase = Depends(get_current_user)):
    return db_user.get_user(db,id)   



