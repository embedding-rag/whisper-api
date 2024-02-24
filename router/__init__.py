from fastapi import APIRouter

from api.transcribe import router as transcribe_router

router = APIRouter()

router.include_router(transcribe_router, tags=["transcribe"])