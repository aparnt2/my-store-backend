# from fastapi import HTTPException,status
from schemas import EmployeeBase,EmployeeUpdate
from db.hash import Hash
from db.models import DbEmployee, DbUser, DbRole, DbDepartment
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


   
def create_employee(db: Session, request: EmployeeBase):
    existing_user = db.query(DbUser).filter(DbUser.username == request.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

  
    existing_phone = db.query(DbEmployee).filter(DbEmployee.phone_no == request.phone_no).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already exists")
    
    
    
    user = DbUser(
        username=request.username,
        password=Hash.bcrypt(request.password),
        sr_id=2,
        is_active = "NO"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

   
    employee = DbEmployee(
        name=request.name,
        phone_no=request.phone_no,
        user_id=user.user_id,
        department_id=request.department_id,
        role_id=request.role_id
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee



def get_all_employees(db:Session):
    return db.query(DbEmployee).all()  

def get_employees(db:Session,emp_id:int):
    employee = db.query(DbEmployee).filter(DbEmployee.emp_id == emp_id).first() 
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with emp_id={emp_id} not found"
        )
    return employee

def update_employee(db: Session, emp_id: int, request: EmployeeUpdate):
   
    employee = db.query(DbEmployee).filter(DbEmployee.emp_id == emp_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    role = db.query(DbRole).filter(DbRole.role_id == request.role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail= "role not found")   

    department = db.query(DbDepartment).filter(DbDepartment.id == request.dept_id).first()
    if not department:
        raise HTTPException(status_code=404, detail= "department not found")  

    existing_phone = db.query(DbEmployee).filter(DbEmployee.phone_no == request.phone_no).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already exists")  
    

    employee.name = request.name
    employee.phone_no = request.phone_no
    employee.role_id = request.role_id
    employee.department_id = request.dept_id

    
    db.commit()
    db.refresh(employee)

    
    return {
        "emp_id": employee.emp_id,
        "name": employee.name,
        "phone_no":employee.phone_no,
         
        "role": {
            "role_id": role.role_id,
            "role_code":role.role_code,
            "role_name":role.role_name,
            
        },
        "department": {
            "id": department.id,
            "code":department.code,
            "name":department.name,
            
        }
    }
     

def delete_employee(db: Session, emp_id: int):
    employee = db.query(DbEmployee).filter(DbEmployee.emp_id == emp_id).first()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with id={emp_id} not found"
        )

    user = db.query(DbUser).filter(DbUser.user_id == employee.user_id).first()

    db.delete(employee)

    if user:
        db.delete(user)

    db.commit()
    return {"message": "Employee and login deleted successfully"}


