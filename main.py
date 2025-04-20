from fastapi import FastAPI
from .database import (
    create_db_and_tables, insert_users_to_db, install_fuzzy_search_extension
)
from .routers import users

app = FastAPI()

app.include_router(users.router)

@app.on_event("startup")
def on_startup():
    users_file_name = "usernames_all.txt"
    create_db_and_tables()
    insert_users_to_db(users_file_name)
    install_fuzzy_search_extension() 

@app.get("/")
async def root():
    return {"message": "Hello World"}