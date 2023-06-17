"""
User Model
"""
from typing import cast
from sqlalchemy import Column, String, Integer
from app.database.postgres.model.common_fields import CommonBase, Base


class User(Base, CommonBase):
    __tablename__ = "user"

    age = cast(int, Column(Integer))
    name = cast(str, Column(String(100), nullable=False))
