
from fastapi import FastAPI
 #from enum import Enum #from typing import Optional
from router import employee,department,role,category,product,file,customer,user
from fastapi.staticfiles import StaticFiles 
from db import models
from auth import authentication
# from fastapi.responses import JSONResponse
from db.database import engine,SessionLocal
# from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

from db.db_admin import seed_admin_user 

app=FastAPI() 



@app.get('/') 
def index():
    return 'product management system'

app.include_router(authentication.router)

app.include_router(file.router)
app.include_router(employee.router)
app.include_router(customer.router)
app.include_router(department.router)
app.include_router(role.router) 
app.include_router(category.router)
app.include_router(product.router)
app.include_router(user.router)

#models.Base.metadata.drop_all(engine)
models.Base.metadata.create_all(engine) 



@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    seed_admin_user(db)   
    db.close()


origins = [
    "http://localhost:5174"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/media", StaticFiles(directory="media"), name="media")