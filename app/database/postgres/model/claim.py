"""
Claim Model
"""
from typing import cast
from sqlalchemy import Column, String, Integer, Float, DateTime
from app.database.postgres.model.common_fields import CommonBase, Base


class Claim(Base, CommonBase):
    __tablename__ = "claim"

    service_date = cast(str, Column(DateTime))
    submitted_procedure = cast(str, Column(String(100), nullable=False))
    quadrant = cast(str, Column(String(100)))
    plan_or_group = cast(str, Column(String(100), nullable=False))
    subscriber = cast(str, Column(String(100), nullable=False))
    provider_npi = cast(str, Column(Float, nullable=False))
    provider_fee = cast(str, Column(Float, nullable=False))
    allowed_fee = cast(str, Column(Float, nullable=False))
    member_coinsurance = cast(str, Column(Float, nullable=False))
    member_copay = cast(str, Column(Float, nullable=False))
    net_fee = cast(float, Column(Float, nullable=False))
