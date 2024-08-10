from fastapi.testclient import TestClient
from fastapi import FastAPI 
from sqlmodel import SQLModel, create_engine, Session
from todo import setting
from todo.main import app , get_session
import pytest


# create the engin for test
connection_string : str = str(setting.TEST_DATABASE_URL).replace("postgresql","postgresql+psycopg")
engine = create_engine(connection_string, connect_args={"sslmode":"require"},pool_recycle=300,echo=True)

#======================================================================================================
# Refector with pytest fixture 
# 4 stages:
# 1: Arange => Arrange teh resourses like creating the table, session , and client
#2 : Act => perform the action what to do
#3 : assert => verify that your Act perform is correct or not
#4 : cleanup => clean up the test code

@pytest.fixture(scope="module", autouse=True)
def get_db_session():
    SQLModel.metadata.create_all(engine)
    yield Session(engine)
    
@pytest.fixture(scope="function")
def test_app(get_db_session):
    def test_session():
        yield get_db_session
    app.dependency_overrides[get_session]= test_session
    with TestClient(app=app) as client:
        yield client
    
 


#======================================================================================================

#test 1: root test
def test_getsomeone():
    client= TestClient(app=app)
    response= client.get("/")
    data= response.json()
    assert response.status_code==200
    assert data== {"message":"hello every one hh nasir"}
    
    
# test 2: post test
def test_create_todos(test_app):
    # SQLModel.metadata.create_all(engine)  # to create the table
    # with Session(engine) as session:      # to create the session 
    #     def db_session_override():
    #         return session  
    # app.dependency_overrides[get_session]= db_session_override   # to override the test seesion on main branch session
    # client = TestClient(app=app)
    test_todo= {"content":"aneela create to test", "is_completed":False}
    response= test_app.post('/todos/', json=test_todo)
    data= response.json()
    assert response.status_code==200
    assert data["content"]== test_todo["content"]
    
    
# test 3:  get_all 
def test_get_all_todos(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
    # app.dependency_overrides[get_session]= db_session_override
    # client= TestClient(app=app)
    test_todo= {"content":"get all todos test", "is_completed":False} # to veryfy create a list
    response= test_app.post('/todos/', json=test_todo)  # post the created list in table
    data= response.json()
    response= test_app.get('/todos') # get all data from table
    new_todos= response.json()[-1]  # to gat the last list that we have posted
    assert response.status_code == 200
    assert new_todos["content"]== test_todo["content"]
    
       
# test 4 : sigle to do
def test_get_single_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
        
    # app.dependency_overrides[get_session]= db_session_override
    # client= TestClient(app=app)
    
    test_todo= {"content":"get single todo test", "is_completed":False}
    response= test_app.post('/todos/', json=test_todo)
    todo_id = response.json()["id"]
    
    res= test_app.get(f'todos/{todo_id}')
    data = res.json()
    assert res.status_code == 200
    assert data["content"] == test_todo["content"]
    
    
    
# test 5: put (edit) todo  test
def test_edit_todo(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
        
    # app.dependency_overrides[get_session]= db_session_override
    # client= TestClient(app=app)
    
    test_todo= {"content":"edit todo test", "is_completed":False}
    response= test_app.post('/todos/', json=test_todo)
    todo_id = response.json()["id"]
    
    eddited_todo= {"content":"We have edited todo test", "is_completed":False}
    response= test_app.put(f'/todos/{todo_id}', json=eddited_todo)
    data= response.json()
    
    assert response.status_code == 200
    assert data["content"]== eddited_todo["content"]
    
    
    
# test 6: Delste todo
def test_delete_todos(test_app):
    # SQLModel.metadata.create_all(engine)
    # with Session(engine) as session:
    #     def db_session_override():
    #         return session
        
    # app.dependency_overrides[get_session]== db_session_override
    # client= TestClient(app=app)
    
    test_todo= {"content":"delete todo test", "is_completed":False}
    response= test_app.post('/todos/', json=test_todo)
    todo_id = response.json()["id"]
    
    response= test_app.delete(f'/todos/{todo_id}')
    data= response.json()
    
    assert response.status_code == 200
    assert data["message"]=="Task successfully Deleted!"
    
    
    
        
    

    
    
    
    
    