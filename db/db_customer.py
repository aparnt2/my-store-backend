
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from db.models import DbUser
from db.hash import Hash

CUSTOMER_ROLE_ID = 3   

def create_customer(db: Session, request):
   
    existing_user = db.query(DbUser).filter(DbUser.username == request.username).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )

    
    new_customer = DbUser(
        username=request.username,
        password=Hash.bcrypt(request.password),
        sr_id=CUSTOMER_ROLE_ID,  
        is_active="NO"
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer
