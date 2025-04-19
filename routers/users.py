from fastapi import APIRouter, HTTPException, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlmodel import select
from typing import Annotated
from ..dependencies import SessionDep
from ..database import User

router = APIRouter(
    prefix="/users",
    # For FastAPI automatic API documentation
    tags=["users"]
)

# Request body that endpoint expects to receive
class UserCreate(BaseModel):
    username: str 
    bio: str | None = None # Optional field, default is None

@router.post("")
def create_new_user(
    request: UserCreate,
    # Dependency injection to get a database session
    session: SessionDep
):
    new_user = User.model_validate(request) 

    existing_user = session.exec(
        select(User)
        .where(User.username == new_user.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create new user. User with username '{new_user.username}' already exists"
        ) 

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user 

@router.delete("/{user_id}")
def delete_user_by_id(
    user_id: int,
    session: SessionDep
):
    user_to_delete = session.exec(
        select(User)
        .where(User.id == user_id)
    ).first()

    if not user_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Failed to delete user. User with id {user_id} does not exist"
        )

    session.delete(user_to_delete)
    session.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": f"Successfully deleted user with id {user_id}"
        }
    )

@router.get("", response_model=list[User])
def read_all_user(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    users_list = session.exec(
        select(User)
        .offset(offset)
        .limit(limit)
        .order_by(User.username.asc())
    ).all()

    return users_list