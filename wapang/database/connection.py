import asyncio
from contextvars import ContextVar, Token
from uuid import uuid4
from sqlalchemy import AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import (
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from wapang.database.settings import DB_SETTINGS


class DatabaseManager:
    def __init__(self):
        # TODO pool 이 뭘까요?
        # pool_recycle 은 뭐고 왜 28000으로 설정해두었을까요?
        self.engine = create_async_engine(
            DB_SETTINGS.url,
            poolclass=AsyncAdaptedQueuePool,
            pool_recycle=28000,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, expire_on_commit=False
        )


DEFAULT_SESSION_ID = "default_session_id"
DEFAULT_SESSION_TASK = "default_session_task"
DEFAULT_SESSION_CONTEXT = (DEFAULT_SESSION_ID, DEFAULT_SESSION_TASK)
session_context_var: ContextVar[tuple[str, str]] = ContextVar(
    "session_context", default=DEFAULT_SESSION_CONTEXT
)


def reset_session_id(token: Token[tuple[str, str]]) -> None:
    session_context_var.reset(token)


def set_session_id() -> Token[tuple[str, str]] | None:
    session_id, session_task = session_context_var.get()
    if session_id == DEFAULT_SESSION_ID or session_task != DEFAULT_SESSION_TASK:
        current_task = asyncio.current_task()
        if current_task is None:
            raise RuntimeError("No current task")
        token = session_context_var.set((str(uuid4()), current_task.get_name()))
        return token


def get_session_id() -> str:
    return session_context_var.get()[0]


SESSION = async_scoped_session(
    session_factory=DatabaseManager().session_factory, scopefunc=get_session_id
)
