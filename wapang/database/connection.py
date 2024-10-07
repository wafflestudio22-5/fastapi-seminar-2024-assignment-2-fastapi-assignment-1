from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from wapang.database.settings import DB_SETTINGS


class DatabaseManager:
    def __init__(self):
        self.engine = create_engine(
            DB_SETTINGS.url,
            pool_recycle=28000,
            pool_pre_ping=True,
        )
        self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)


# 아래 함수를 이용해서 Session 종속성을 주입받을 수 있습니다.
def get_db_session() -> Generator[Session]:
    session = DatabaseManager().session_factory()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
