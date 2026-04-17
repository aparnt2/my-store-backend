from schemas import CategoryBase
from db.models import DbCategory,DbProduct
from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from utils.string_utils import normalize_string

def create_category(db: Session, request: CategoryBase):
   

    if not request.category_name or not request.category_name.strip() or request.category_name.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name cannot be empty or default value"
    )

    normalized_name = normalize_string(request.category_name)
   
    existing_categories = db.query(DbCategory).all()
    for category in existing_categories:
       if normalize_string(category.category_name) == normalized_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists"
        )
    new_category = DbCategory(
       
        category_name = request.category_name,
        image_url=request.image_url
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

def get_all_categories(db:Session):
    return db.query(DbCategory).all()     

def get_category(db:Session,id:int):
    category = db.query(DbCategory).filter(DbCategory.category_id == id).first() 
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Category with id={id} not found"
        )
    return category


def update_category(db: Session, id: int, request: CategoryBase):
    category = db.query(DbCategory).filter(DbCategory.category_id == id).first()
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with id={id} not found"
        )

    
    if not request.category_name or not request.category_name.strip() or request.category_name.strip().lower() == "string":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name cannot be empty or default value"
        )

    normalized_name = normalize_string(request.category_name)

   
    existing_categories = db.query(DbCategory).filter(DbCategory.category_id != id).all()
    for c in existing_categories:
        if normalize_string(c.category_name) == normalized_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists"
            )

   
    category.category_name = request.category_name.strip()
    category.image_url = request.image_url.strip() if request.image_url else None

    db.commit()
    db.refresh(category)

    return {
        "category_id": category.category_id,
        "category_name": category.category_name,
        "image_url": category.image_url
    }

def delete_category(db:Session,id:int):
    category = db.query(DbCategory).filter(DbCategory.category_id == id).first()  
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with id={id} not found"
        )
    product_count = db.query(DbProduct).filter(
        DbProduct.category_id == id).count()

    if product_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This category has products. Move or delete them first."
        )
    
    db.delete(category)
    db.commit()
    return 'ok'    