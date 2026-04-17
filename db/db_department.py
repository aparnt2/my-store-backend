from schemas import DepartmentBase
from db.models import DbDepartment,DbEmployee
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from utils.string_utils import normalize_string

def create_dept(db: Session, request: DepartmentBase):
   

    if not request.code or not request.code.strip() or request.code.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department code cannot be empty or default value"
        )


    if not request.name or not request.name.strip() or request.name.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name cannot be empty or default value"
    )
    
    normalized_code = normalize_string(request.code)
    normalized_name = normalize_string(request.name)


    if db.query(DbDepartment).filter(DbDepartment.code.ilike(normalized_code)).first():
       raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Department code already exists"
    )


    existing_departments = db.query(DbDepartment).all()
    for dept in existing_departments:
       if normalize_string(dept.name) == normalized_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name already exists"
        )
    new_dept = DbDepartment(
        code=request.code.strip(),
        name = request.name.strip()
    )
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept

def get_all_depts(db:Session):
    return db.query(DbDepartment).all() 

def get_dept(db:Session,id:int):
    dept = db.query(DbDepartment).filter(DbDepartment.id == id).first()  
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id={id} not found"
        )
    return dept

def update_dept(db: Session, id: int, request: DepartmentBase):
    
    
    dept = db.query(DbDepartment).filter(DbDepartment.id == id).first()
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Department with id={id} not found"
        )

  
    if not request.code or not request.code.strip() or request.code.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department code cannot be empty or default value"
        )

    if not request.name or not request.name.strip() or request.name.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Department name cannot be empty or default value"
        )

    normalized_code = normalize_string(request.code)
    normalized_name = normalize_string(request.name)

    
    existing_departments = db.query(DbDepartment).filter(DbDepartment.id != id).all()
    for d in existing_departments:
        if normalize_string(d.code) == normalized_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department code already exists"
            )
        if normalize_string(d.name) == normalized_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department name already exists"
            )

    
    dept.code = request.code.strip()
    dept.name = request.name.strip()

    db.commit()
    db.refresh(dept)

    return {
        "id": dept.id,
        "code": dept.code,
        "name": dept.name
    }

def delete_dept(db:Session,id:int):
    
    dept = db.query(DbDepartment).filter(DbDepartment.id == id).first()  
    if not dept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Department with id={id} not found"
        )
    employee_count = db.query(DbEmployee).filter(
        DbEmployee.department_id == id).count()

    if employee_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This department has employees. Move or delete them first."
        )        
    db.delete(dept)
    db.commit()
    return 'ok' 