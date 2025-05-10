from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
import os
from dotenv import load_dotenv
from pydantic import EmailStr
from datetime import datetime, timezone

load_dotenv()

# Database table
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, max_length=30)
    bio: str | None = Field(default="This is my bio")
    profile_picture: str | None = Field(default="https://i.imgur.com/vIaC7Uq.png")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

PSQL_URI = os.getenv("PSQL_URI")
engine = create_engine(PSQL_URI)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def insert_users_to_db(filename: str):
    with Session(engine) as session:
        users_list = session.exec(
            select(User)
        ).all()
        if len(users_list) > 0:
            print("Users database populated. Skipping user import.")
            return

    print("Populating users from txt file")

    with open(filename, newline="", encoding="utf-8") as file:
        usernames_list = [line.strip() for line in file]
        with Session(engine) as session:
            for username in usernames_list:
                new_user = User(username=username)
                try:
                    session.add(new_user)
                    session.commit()
                    session.refresh(new_user)
                    print("User added: ", new_user)
                except IntegrityError as e:
                    session.rollback()  # Rollback the transaction if there's an error
                    print(f"Error adding user '{username}': {e.orig}") 

def install_fuzzy_search_extension():
    with Session(engine) as session:
        print("Verifying installation for PSQL fuzzy search extension...")
        try:
            session.exec(text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
            session.commit()
            print("Extension pg_trgm installed successfully.")
        except Exception as e:
            print(f"Error installing extension: {e}")