from fastapi import FastAPI, APIRouter


router = APIRouter()

@router.get("/health")
async def health_check() -> dict:
    return {"status": "Reports OK"}
