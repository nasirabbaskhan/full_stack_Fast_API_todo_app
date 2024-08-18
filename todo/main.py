
from fastapi import FastAPI ,Depends, HTTPException
import uvicorn 
from todo import setting
from sqlmodel import SQLModel , create_engine , Session,select
from typing import Annotated
from contextlib import asynccontextmanager
from todo.model import Todo, Todo_Create, Todo_Edit


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
    return {"message":"Wellcome to our Todo App with CRUD functionality"}

 
 


@app.post("/todos/",response_model=Todo)
async def create_todos(todo:Todo_Create, session:Annotated[Session, Depends(get_session)] ):
    new_todo = Todo(content=todo.content)
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo
    

@app.get("/todos/",response_model=list[Todo])
async def get_all_todos(session:Annotated[Session, Depends(get_session)]):
   
    todos= session.exec(select(Todo)).all()
    return todos
    
    
@app.get("/todos/{id}")
async def get_single_todo(id:int,session:Annotated[Session, Depends(get_session)]):
    user_todo= session.exec(select(Todo).where(Todo.id==id)).first()
    
    if user_todo:
        return user_todo
    else:
        raise HTTPException(status_code=404, detail="No Task found")
        
    
   
   

@app.put("/todos/{id}")
async def edit_todo( id:int,todo:Todo_Edit,
                    session:Annotated[Session, Depends(get_session)]):
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
    todo= session.exec(select(Todo).where(Todo.id==id)).first() # it will return array so we have nedd to run the loop
    
    if todo:
        session.delete(todo)
        session.commit()
        # session.refresh(todo)
        return {"message":"Task successfully Deleted!"}
    else:
        raise HTTPException (status_code=404, detail="No task found")



# function to start the server   
def start():
    uvicorn.run("todo.main:app",host="0.0.0.0", port=8000, reload=True)