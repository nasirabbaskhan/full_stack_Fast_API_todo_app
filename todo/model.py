from pydantic import BaseModel
from sqlmodel import SQLModel, Field 
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm 
from typing import Annotated


#4: create the model
 # data model (data validation using pydantic model)
 # table model (table creation)
class Todo (SQLModel, table=True):
    id:int | None= Field(default=None, primary_key=True)
    content: str = Field(index=True, min_length=4, max_length=50)
    is_completed : bool = Field(default=False)
    
    
# data model (data validation using pydantic model)
class Todo_Create (BaseModel):
    content: str = Field(index=True, min_length=4, max_length=50)
    

# data model (data validation using pydantic model)
class Todo_Edit(BaseModel):
     content: str 
     is_completed : bool
     
