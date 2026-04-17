

from schemas import CategoryBase, CategoryDisplay,CategoryList

from fastapi import APIRouter,Depends,Request
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_category

router=APIRouter(
    prefix='/category',
    tags=['category']
)

#create role

@router.post('/',response_model = CategoryDisplay)
def create_category(request : CategoryBase,db:Session = Depends(get_db)):
     return db_category.create_category(db,request)

@router.get('/',response_model=CategoryList)
def get_all_categories(request:Request,db:Session = Depends(get_db)):
    categories= db_category.get_all_categories(db)
    # return {
    #     "categories": [
    #         {
    #             "category_id": category.category_id,
    #             "category_code": category.category_code,
    #             "category_name": category.category_name,
    #             "image_url": category.image_url
    #         } for category in categories
    #     ]
    # }
    for c in categories:
        if c.image_url and not c.image_url.startswith("http"):
            c.image_url = (
                str(request.base_url)
                + f"media/categories/{c.image_url}"
            )

    return {
        "categories": categories
    }
@router.get('/{id}',response_model=CategoryDisplay)   
def get_category(id:int,db:Session = Depends(get_db)):
    return db_category.get_category(db,id)   


@router.post("/{id}/update",response_model=CategoryDisplay)
def update_category(id:int,request:CategoryBase,db:Session = Depends(get_db)):
    return db_category.update_category(db,id,request)    

@router.get("/{id}/delete")
def delete_category(id:int,db:Session = Depends(get_db)):
    return db_category.delete_category(db,id)       