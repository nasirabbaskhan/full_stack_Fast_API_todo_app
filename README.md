# Pckages

poetry add fastapi

poetry add uvicorn

poetry oadd sqlmdel

poetry add "psycopg[binary]"

poetry add psycopg2-binary 

### if show the import problem

`poetry env info --path `

select the path  and enter in `Python:select interpreter`

# for CRUD operation

step 1: Create Database on Neon

step 2: Create .env file for environment variable 

step 3: Create setting.py file for encrypting DatabaseURL

step 4: Create a Model in model.py file 

step 5: Create Engine in db.py file

step 6: Create Function for table ceation in db.py file  

step 7: Create Function for session management in db.py file 
 
step 8: Create context manager for app lifespan in main file 

step 9: Create all endpoints of todo app in main file


## for Test fast API

poetry add pytest

poetry add httpx

To run the test
`poetry run pytest`



