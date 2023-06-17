from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel
from typing import Optional


class ClaimBase(BaseModel):
    service_date: str
    submitted_procedure: str
    quadrant: str
    plan_or_group: str
    subscriber: str
    provider_npi: float
    provider_fee: float
    allowed_fee: float
    member_coinsurance: float
    member_copay: float


class ClaimRequest(ClaimBase):
    pass


class ClaimResponse(ClaimBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    service_date: datetime
    net_fee: float

    class Config:
        orm_mode = True
