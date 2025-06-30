from contextlib import asynccontextmanager
from typing import AsyncIterator

from pydantic import PostgresDsn
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class SQLAlchemyClient:
    def __init__(self, app_db_url: PostgresDsn):
        self.app_db_url = app_db_url
        self.engine = create_async_engine(str(app_db_url))
        self.session_maker = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    def close(self):
        try:
            self.session_maker.close_all()
            self.engine.dispose()
        finally:
            self.engine = None

    @asynccontextmanager
    async def make_session(self) -> AsyncIterator[AsyncSession]:
        async with self.session_maker() as session:
            yield session

    @staticmethod
    def init_select_estoque(base_class) -> select:
        s = select(base_class)
        return s

    @staticmethod
    def init_delete_estoque(base_class) -> delete:
        d = delete(base_class)
        return d

    @staticmethod
    def to_dict(base) -> dict | None:
        if base is None:
            return None
        d = base.__dict__
        d.pop("_sa_instance_state", None)
        return d

    @staticmethod
    def get_pk_fields(base_class) -> list[str]:
        pk_fields = [column.name for column in base_class.__table__.columns if column.primary_key]
        return pk_fields