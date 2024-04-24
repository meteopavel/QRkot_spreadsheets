from fastapi import APIRouter

from app.api.endpoints import (
    google_api_router, charity_router, donation_router, user_router
)


main_router = APIRouter()
main_router.include_router(
    charity_router, prefix='/charity_project',
    tags=['Благотворительные проекты']
)
main_router.include_router(
    donation_router, prefix='/donation',
    tags=['Пожертвования']
)
main_router.include_router(
    google_api_router, prefix='/google',
    tags=['Google']
)
main_router.include_router(user_router)
