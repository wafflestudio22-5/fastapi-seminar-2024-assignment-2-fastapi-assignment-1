from wapang.database.connection import SESSION, reset_session_id, set_session_id


from functools import wraps
from typing import Awaitable, Callable, ParamSpec, TypeVar

P = ParamSpec("P")
RT = TypeVar("RT")


def transactional(f: Callable[P, Awaitable[RT]]) -> Callable[P, Awaitable[RT]]:
    @wraps(f)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> RT:
        tokens = set_session_id()
        try:
            ret = await f(*args, **kwargs)
        except Exception as e:
            if tokens:
                await SESSION.rollback()
            raise e
        else:
            if tokens:
                await SESSION.commit()
        finally:
            if tokens:
                await SESSION.close()
                reset_session_id(tokens)
        return ret

    return wrapper
