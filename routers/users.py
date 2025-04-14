from fastapi import APIRouter 

router = APIRouter(
    prefix="/users",
    # For FastAPI automatic API documentation
    tags=["users"]
)
