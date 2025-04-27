from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import (
    create_db_and_tables, insert_users_to_db, install_fuzzy_search_extension,
)
from .routers import users
from .search_service import username_search_service

app = FastAPI()

# Origins allowed to call this backend API
origins = [
    # Local frontend URL 
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

@app.on_event("startup")
def on_startup():
    users_file_name = "usernames_all.txt"
    create_db_and_tables()
    insert_users_to_db(users_file_name)
    install_fuzzy_search_extension() 

    # Build initial TF-IDF index
    username_search_service.rebuild_index()

@app.get("/")
async def root():
    return {"message": "Hello World"}