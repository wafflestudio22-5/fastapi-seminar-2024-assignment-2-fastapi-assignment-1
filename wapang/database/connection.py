import asyncio
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request

from wapang.common.utils import get_request_id
from wapang.database.settings import DB_SETTINGS


class DatabaseManager:
    def __init__(self):
        # TODO pool 이 뭘까요?
        # pool_recycle 은 뭐고 왜 28000으로 설정해두었을까요?
        self.engine = create_async_engine(
            DB_SETTINGS.url,
            pool_recycle=28000,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )


SESSION = async_scoped_session(
    session_factory=DatabaseManager().session_factory, scopefunc=get_request_id
)


class DbSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        try:
            response = await call_next(request)
        except Exception as e:
            await SESSION.rollback()
            raise e
        else:
            await SESSION.commit()
        finally:
            await SESSION.close()
        return response
