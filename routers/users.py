from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from sqlmodel import select
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

