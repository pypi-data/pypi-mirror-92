from typing import Optional

import pydantic
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class BaseORM:
    """
    Base object relational mapper for associating user-defined Python classes with database tables
    """
    id = Column(String(36), primary_key=True)


class BaseModel(pydantic.BaseModel):
    """
    Base model for data container, validation and mapping between ORM
    """
    id: Optional[str] = None

    class Config:
        orm_mode = True
