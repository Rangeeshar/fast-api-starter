"""
Common Fields Model like id, created_at etc..
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, cast, Optional

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CommonBase:
    __tablename__ = "common_base"
    # change your schema here
    # __table_args__ = ({'schema': 'core_schema'})

    id = cast(
        UUID(as_uuid=True),
        Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True),
    )  # type: ignore
    created_by = cast(Optional[str], Column(String))
    created_at = cast(
        datetime, Column(DateTime(timezone=False), default=datetime.utcnow)
    )
    updated_by = cast(Optional[str], Column(String))
    updated_at = cast(
        datetime,
        Column(
            DateTime(timezone=False), default=datetime.utcnow, onupdate=datetime.utcnow
        ),
    )
    context = cast(Optional[str], Column(String))
    """Base class used for model definitions.

    Provides convenience methods that can be used to convert model
    to the corresponding schema.
    """

    @classmethod
    def schema(cls) -> str:
        """Return name of database schema the model refers to."""

        _schema = cls.__mapper__.selectable.schema
        if _schema is None:
            raise ValueError("Cannot identify model schema")
        return _schema

    @classmethod
    def table_name(cls) -> str:
        """Return name of the table the model refers to."""

        return cls.__tablename__

    @classmethod
    def fields(cls) -> List[str]:
        """Return list of model field names."""

        return cls.__mapper__.selectable.c.keys()

    def to_dict(self) -> Dict[str, Any]:
        """Convert model instance to a dictionary."""

        _dict: Dict[str, Any] = dict()
        for key in self.__mapper__.c.keys():
            _dict[key] = getattr(self, key)
        return _dict
