

from schemas import RoleBase,RoleDisplay,RoleList
from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_role

router=APIRouter(
    prefix='/role',
    tags=['role']
)

#create role

@router.post('/',response_model=RoleDisplay)
def create_role(request : RoleBase,db:Session = Depends(get_db)):
     return db_role.create_role(db,request)

@router.get('/',response_model=RoleList)
def get_all_roles(db:Session = Depends(get_db)):
    roles= db_role.get_all_roles(db)
    return {
        "roles": [
            {
                "role_id": role.role_id,
                "role_code": role.role_code,
                "role_name": role.role_name
            } for role in roles
        ]
    }

@router.get('/{id}',response_model=RoleDisplay)   
def get_role(id:int,db:Session = Depends(get_db)):
    return db_role.get_role(db,id)   

@router.post("/{id}/update",response_model=RoleDisplay)
def update_role(id:int,request:RoleBase,db:Session = Depends(get_db)):
    return db_role.update_role(db,id,request)    

@router.get("/{id}/delete")
def delete_role(id:int,db:Session = Depends(get_db)):
    return db_role.delete_role(db,id)    





