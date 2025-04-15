from fastapi import FastAPI
from .database import create_db_and_tables, insert_users_to_db
from .routers import users

app = FastAPI()

app.include_router(users.router)

@app.on_event("startup")
def on_startup():
    users_file_name = "usernames_all.txt"
    create_db_and_tables()
    insert_users_to_db(users_file_name)

@app.get("/")
async def root():
    return {"message": "Hello World"}