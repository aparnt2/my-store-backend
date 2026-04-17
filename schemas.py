
from __future__ import annotations
from pydantic import BaseModel,Field
from typing import List,Optional
from datetime import datetime 

class DepartmentBase(BaseModel):
    #id:int
    code:str
    name:str

class DepartmentDisplay(BaseModel):
    id: int
    code: str
    name: str
    class Config():
        orm_mode = True

class DepartmentList(BaseModel):
    departments: List[DepartmentDisplay]

class RoleBase(BaseModel):
    role_code:str
    role_name:str    

class RoleDisplay(BaseModel):
    role_id: int
    role_code: str
    role_name: str
    class Config():
        orm_mode = True

class RoleList(BaseModel):
    roles: List[RoleDisplay]    

class CategoryBase(BaseModel):
    # category_code : str
    category_name : str   
    image_url: str

class CategoryDisplay(BaseModel):
    category_id: int
    # category_code: str
    category_name: str
    image_url: str
    class Config():
        orm_mode = True 

class CategoryList(BaseModel):
    categories: List[CategoryDisplay]  

class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    image_url: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)
    
class ProductDisplay(BaseModel):
    product_id: int
    product_name: str
    description: str
    price: float
    stock: int
    category: CategoryDisplay 
    image_url: str
    created_at: datetime
    class Config():
        orm_mode = True

# class ProductByCategory(BaseModel):
#     product_id: int
#     product_name: str
#     description: str
#     price: float
#     stock: int
#     image_url: str
#     created_at: datetime
    # category_id: Optional[int]  

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username : str
    password : str    
    

class UserDisplay(BaseModel):
    user_id: int
    username: str
    sr_id : int
    is_active: str
    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    username:str
    password:str
    name: str
    phone_no: str
    # user_id: int
    role_id: int
    department_id: int

class EmployeeDisplay(BaseModel):
    emp_id: int
    name: str
    phone_no: str
    user: UserDisplay
    role: RoleDisplay
    department: DepartmentDisplay

    class Config:
        orm_mode = True

class EmployeeUpdate(BaseModel):
    name: str
    phone_no: int
    role_id: int
    dept_id: int 

class EmployeeUpdateDisplay(BaseModel):
    emp_id: int
    name: str
    phone_no: str
    role: RoleDisplay
    department: DepartmentDisplay

    class Config:
        orm_mode = True

class CustomerCreate(BaseModel):
    username : str
    password : str         
