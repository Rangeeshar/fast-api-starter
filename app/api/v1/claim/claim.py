"""
Claim endpoints
===============
Consist of claims which will perform claim CRUD operations using various endpoints.
"""
from http import HTTPStatus
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db.deps import get_db
from app.database.postgres.model.claim import Claim
from app.services.v1.claim import claim_service
from app.services.v1.claim.claim_schema import ClaimResponse, ClaimRequest

api_router = APIRouter()


@api_router.post("", response_model=ClaimResponse, status_code=HTTPStatus.CREATED)
async def create_user(
    claim_request: ClaimRequest, db: Session = Depends(get_db)
) -> ClaimResponse:
    claim: Optional[Claim] = claim_service.create_claim(
        claim_request=claim_request, db=db
    )
    return claim


@api_router.get("", response_model=List[ClaimResponse])
async def get_users(db: Session = Depends(get_db)) -> List[ClaimResponse]:
    return claim_service.get_claims(db=db)


@api_router.get("/{_id}", response_model=ClaimResponse)
async def get_claim_by_id(_id: UUID, db: Session = Depends(get_db)) -> ClaimResponse:
    return claim_service.get_claim_by_id(_id=_id, db=db)


@api_router.put("/{_id}", response_model=ClaimResponse, status_code=HTTPStatus.OK)
async def update_claim(
    _id: UUID, claim_request: ClaimRequest, db: Session = Depends(get_db)
) -> ClaimResponse:
    user: Optional[Claim] = claim_service.update_claim(
        _id=_id, claim_request=claim_request, db=db
    )
    return user


@api_router.delete("/{_id}", status_code=HTTPStatus.OK)
async def delete_claim_by_id(_id: UUID, db: Session = Depends(get_db)):
    claim_service.delete_claim_by_id(_id=_id, db=db)
