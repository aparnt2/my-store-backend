

from schemas import RoleBase
from db.models import DbRole,DbEmployee
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from utils.string_utils import normalize_string

def create_role(db: Session, request: RoleBase):
    

    if not request.role_code or not request.role_code.strip() or request.role_code.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role code cannot be empty or default value"
        )


    if not request.role_name or not request.role_name.strip() or request.role_name.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role name cannot be empty or default value"
    )
    normalized_code = normalize_string(request.role_code)
    normalized_name = normalize_string(request.role_name)


    if db.query(DbRole).filter(DbRole.role_code.ilike(normalized_code)).first():
       raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Role code already exists"
    )


    existing_roles = db.query(DbRole).all()
    for role in existing_roles:
       if normalize_string(role.role_name) == normalized_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role name already exists"
        )

    

    new_role = DbRole(
        role_code=request.role_code,
        role_name = request.role_name
    )
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    return new_role

def get_all_roles(db:Session):
    return db.query(DbRole).all() 

def get_role(db:Session,id:int):
    role = db.query(DbRole).filter(DbRole.role_id == id).first() 
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id={id} not found"
        )
    return role

def update_role(db: Session, id: int, request: RoleBase):
    role = db.query(DbRole).filter(DbRole.role_id == id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with id={id} not found"
        )

   
    if not request.role_code or not request.role_code.strip() or request.role_code.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role code cannot be empty or default value"
        )

    if not request.role_name or not request.role_name.strip() or request.role_name.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role name cannot be empty or default value"
        )

    normalized_code = normalize_string(request.role_code)
    normalized_name = normalize_string(request.role_name)

   
    existing_roles = db.query(DbRole).filter(DbRole.role_id != id).all()
    for r in existing_roles:
        if normalize_string(r.role_code) == normalized_code:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role code already exists"
            )
        if normalize_string(r.role_name) == normalized_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role name already exists"
            )

  
    role.role_code = request.role_code.strip()
    role.role_name = request.role_name.strip()

    db.commit()
    db.refresh(role)

    return {
        "role_id": role.role_id,
        "role_code": role.role_code,
        "role_name": role.role_name
    }

def delete_role(db:Session,id:int):
    role = db.query(DbRole).filter(DbRole.role_id == id).first()  
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Role with id={id} not found"
        )
    employee_count = db.query(DbEmployee).filter(
        DbEmployee.role_id == id).count()

    if employee_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This role has employees. Move or delete them first."
        )    
    db.delete(role)
    db.commit()
    return 'ok' 