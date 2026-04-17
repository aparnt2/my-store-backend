from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status
from db.database import get_db
from fastapi.param_functions import Depends
from db import models
from sqlalchemy.orm.session import Session
from db.hash import Hash
from auth import token_utils
# from auth.active_users import current_logged_in_ids, set_active_user
from fastapi.security import OAuth2PasswordBearer
from auth.token_utils import get_current_user 

router = APIRouter(
    tags=['authentication']
)

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/token")

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

   
    user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Account doesn't Exist ")

    
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")

   
    

    user.is_active = "YES"
    db.commit()
    db.refresh(user)

    # current_logged_in_ids.add(user.user_id)
    # set_active_user(db)

    
    access_token = token_utils.create_access_token(
        data={
            "username": user.username,
            "user_id": user.user_id,
            
            "sr_id": user.sr_id 
              }
    )

   
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
        "sr_id": user.sr_id,
        "is_active": "YES"
    }

# @router.post("/logout")
# def logout_user(user_id: int, db: Session = Depends(get_db)):
#     current_logged_in_ids.discard(user_id)
#     set_active_user(db)
#     return {"msg": f"User {user_id} logged out successfully"}
# 
@router.post("/logout")
def logout(user: models.DbUser = Depends(get_current_user), db: Session = Depends(get_db)):
    # user is already authenticated by get_current_user
    user.is_active = "NO"
    db.commit()
    db.refresh(user)

    return {"message": f"User {user.username} logged out successfully"}