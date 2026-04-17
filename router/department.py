
from schemas import DepartmentBase,DepartmentDisplay,DepartmentList
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_department
from typing import List

router=APIRouter(
    prefix='/department',
    tags=['department']
)

#create dept

@router.post('/',response_model=DepartmentDisplay)
def create_dept(request : DepartmentBase,db:Session = Depends(get_db)):
     return db_department.create_dept(db,request)
    # return {
    #     "id": dept.dept_id,
    #     "code": dept.dept_code,
    #     "name": dept.dept_name
    # }

#Read all depts

@router.get('/',response_model=DepartmentList)
def get_all_depts(db:Session = Depends(get_db)):
    departments= db_department.get_all_depts(db)
    return {
        "departments": [
            {
                "id": dept.id,
                "code": dept.code,
                "name": dept.name
            } for dept in departments
        ]
    }

#Read one dept
@router.get('/{id}',response_model=DepartmentDisplay)   
def get_dept(id:int,db:Session = Depends(get_db)):
    return db_department.get_dept(db,id)
      
    # return {
    #     "id": dept.id,
    #     "code": dept.code,
    #     "name": dept.name
    # }

#update the dept
@router.post("/{id}/update",response_model=DepartmentDisplay)
def update_dept(id:int,request:DepartmentBase,db:Session = Depends(get_db)):
    return db_department.update_dept(db,id,request)
      

#delete dept
@router.get("/{id}/delete")
def delete_dept(id:int,db:Session = Depends(get_db)):
    return db_department.delete_dept(db,id)
    
   

