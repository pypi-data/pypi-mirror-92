from typing import Generic, TypeVar, Type, Callable, Optional, List

from sqlalchemy.orm import Session

from coresvc.base.base_model import BaseORM

ORMType = TypeVar("ORMType", bound=BaseORM)


class BaseCrudSql(Generic[ORMType]):
    def __init__(self, session_context: Callable[[], Session], orm_class: Type[ORMType]):
        """
        Base CRUD with db session to Create, Read, Update, Delete
        """
        self.session_context = session_context
        self.orm_class = orm_class

    def create(self, orm_obj: ORMType) -> ORMType:
        with self.session_context() as session:
            session.add(orm_obj)
            session.commit()
            session.refresh(orm_obj)
            return orm_obj

    def read(self, _id: str) -> Optional[ORMType]:
        with self.session_context() as session:
            return session.query(self.orm_class).filter(self.orm_class.id == _id).first()

    def read_multi(self, skip: int = 0, limit: int = 100) -> List[ORMType]:
        with self.session_context() as session:
            return session.query(self.orm_class).offset(skip).limit(limit).all()

    def update(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError
