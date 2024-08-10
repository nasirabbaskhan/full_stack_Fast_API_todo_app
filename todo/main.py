from fastapi import FastAPI ,Depends, HTTPException
import uvicorn 
from sqlmodel import SQLModel, Field , create_engine, Session, select
from todo import setting
from typing import Annotated
from contextlib import asynccontextmanager

# step 1: Create Database on Neon
# step 2: Create .env file for environment variable 
# step 3: Create setting.py file for encrypting DatabaseURL
# step 4: Create a Model in main file
# step 5: Create Engine 
# step 6: Create Function for table ceation 
# step 7: Create Function for session management
# step 8: Create context manager for app lifespan
# step 9: Create all endpoints of todo app


#4: create the model
 # data model (data validation using pydantic model)
 # table model (table creation)

class Todo (SQLModel, table=True):
    id:int | None= Field(default=None, primary_key=True)
    content: str = Field(index=True, min_length=4, max_length=50)
    is_completed : bool = Field(default=False)
    

#5: create the engin : engine is one for whole application   
connection_string : str = str(setting.DATABASE_URL).replace("postgresql","postgresql+psycopg")
engine = create_engine(connection_string, connect_args={"sslmode":"require"},pool_recycle=300,echo=True)

#6: create the table
def create_tables():
    SQLModel.metadata.create_all(engine)

    



#7: session: seperate session for each functionality/transactio
def get_session(): # create function as dependence 
    with Session(engine) as session:  # create session like session= Session(engine)
        yield session # generated function that return the session
        
 #8 this function run firstly after app runs   
@asynccontextmanager              
async def lifespan(app:FastAPI):
    print("creating tables")
    create_tables()
    print("tabl create")
    yield
    
    
# fast api application
app:FastAPI= FastAPI(lifespan=lifespan, title="Todo app", version ="1.0.0")

#9 creating end points
@app.get("/")
async def getsomeone():
    return {"message":"hello every one hh nasir"}


@app.post("/todos/",response_model=Todo)
async def create_todos(todo:Todo, session:Annotated[Session, Depends(get_session)] ):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
    

@app.get("/todos/",response_model=list[Todo])
async def get_all_todos(session:Annotated[Session, Depends(get_session)]):
    statement= select(Todo)
    todos= session.exec(statement).all()
    return todos
    
    
@app.get("/todos/{id}")
async def get_single_todo(id:int, session:Annotated[Session, Depends(get_session)]):
    todo= session.exec(select(Todo).where(Todo.id==id)).first()
    return todo
   
   

@app.put("/todos/{id}")
async def edit_todo(todo:Todo, id:int, session:Annotated[Session, Depends(get_session)]):
    existing_todo= session.exec(select(Todo).where(Todo.id==id)).first()
    if existing_todo:
        existing_todo.content= todo.content
        existing_todo.is_completed=todo.is_completed
        session.add(existing_todo)
        session.commit()
        session.refresh(existing_todo)
        return existing_todo
    else:
        raise HTTPException (status_code=404, detail="No task found")
         
        

@app.delete("/todos/{id}")
async def delete_todos(id:int, session:Annotated[Session, Depends(get_session)]):
    todo= session.exec(select(Todo).where(Todo.id==id)).first()
    if todo:
        session.delete(todo)
        session.commit()
        # session.refresh(todo)
        return {"message":"Task successfully Deleted!"}
    else:
        raise HTTPException (status_code=404, detail="task is not Deleted")



# function to start the server   
def start():
    uvicorn.run("todo.main:app",host="0.0.0.0", port=8000, reload=True)