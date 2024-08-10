# for CRUD operation
poetry add fastapi
poetry add uvicorn
poetry add sqlmodel
poetry add "psycopg[binary]"
poetry add psycopg2-binary 

# if show the import problem
`poetry env info --path `
`C:\Users\Nasir\AppData\Local\pypoetry\Cache\virtualenvs\todo-DfjI-MGT-py3.12`
select the path  and enter in `Python:select interpreter`


step 1: Create Database on Neon

step 2: Create .env file for environment variable 

step 3: Create setting.py file for encrypting DatabaseURL

step 4: Create a Model in main file

step 5: Create Engine 

step 6: Create Function for table ceation 

step 7: Create Function for session management

step 8: Create context manager for app lifespan

step 9: Create all endpoints of todo app


# for Test fast API

poetry add pytest
poetry add httpx

To run the test
`poetry run pytest`
