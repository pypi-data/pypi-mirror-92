from contextlib import contextmanager
from typing import ContextManager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from coresvc.base.base_model import BaseORM


class DatabaseSql:
    def __init__(self, uri):
        self.engine = create_engine(uri, pool_pre_ping=True)
        self.session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_tables(self):
        BaseORM.metadata.create_all(self.engine)

    @contextmanager
    def session_context(self) -> ContextManager[Session]:
        """Provide a transactional scope around a series of operations."""
        session: Session = self.session_maker()
        try:
            yield session
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
