from fastapi import APIRouter

from app.api.v1.claim import claim

api_router = APIRouter(tags=["CRUD APIs"])
api_router.include_router(claim.api_router, prefix="/claim")
