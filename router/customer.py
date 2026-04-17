
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas import CustomerCreate,UserDisplay
from db import db_customer

router = APIRouter(
    prefix="/customer",
    tags=["Customer"]
)

@router.post("/register",response_model=UserDisplay)
def register_customer(request: CustomerCreate, db: Session = Depends(get_db)):
    return db_customer.create_customer(db, request)
