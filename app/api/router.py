from fastapi import APIRouter

from app.api.v1.profile import router as profile_router
from app.api.v1.compare import router as compare_router


api_router = APIRouter(
    prefix="/api/v1"
)

api_router.include_router(profile_router)
api_router.include_router(compare_router)