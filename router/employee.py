
from schemas import EmployeeBase,EmployeeDisplay,EmployeeUpdate,EmployeeUpdateDisplay
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_employee
from typing import List
from auth.dependencies import admin_only,admin_or_employee
router=APIRouter(
    prefix='/employee',
    tags=['employee']
)

#create dept

@router.post('/',response_model=EmployeeDisplay)
def create_employee(request : EmployeeBase,db:Session = Depends(get_db),current_user=Depends(admin_only)):
     return db_employee.create_employee(db,request)

@router.get('/all',response_model=List[EmployeeDisplay])
def get_all_employees(db:Session = Depends(get_db),current_user=Depends(admin_or_employee)):  
    return db_employee.get_all_employees(db)   

@router.get('/{emp_id}',response_model=EmployeeDisplay)  
def get_employees(emp_id:int,db:Session = Depends(get_db),current_user=Depends(admin_or_employee)): 
    return db_employee.get_employees(db,emp_id)  

# @router.post("/{emp_id}", response_model=EmployeeDisplay)
# def update_employee(
#     emp_id: int,
#     request: EmployeeUpdate,
#     db: Session = Depends(get_db)
# ):
#     return db_employee.update_employee(db, emp_id, request)    
@router.post("/{emp_id}/update", response_model=EmployeeUpdateDisplay)
def update_employee(emp_id: int, request: EmployeeUpdate, db: Session = Depends(get_db),current_user=Depends(admin_only)):
    return db_employee.update_employee(db, emp_id, request)


@router.post("/{emp_id}/delete")
def delete_employee(emp_id:int,db:Session = Depends(get_db),current_user=Depends(admin_only)):
    return db_employee.delete_employee(db,emp_id)    