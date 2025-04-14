from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine
import os
from dotenv import load_dotenv
from pydantic import EmailStr
from datetime import datetime, timezone

load_dotenv()

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    bio: str = Field(default="This is my bio")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

PSQL_URI = os.getenv("PSQL_URI")
engine = create_engine(PSQL_URI)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session