from fastapi import FastAPI, Request
from fastapi.exception_handlers import request_validation_exception_handler
from fastapi.exceptions import RequestValidationError

from wapang.api import api_router
from wapang.common.errors import MissingRequiredFieldError

app = FastAPI()

app.include_router(api_router, prefix="/api")

async def clone_async_iterator(ai):
    cache = []
    async for item in ai:
        cache.append(item)
    
    async def gen():
        for item in cache:
            yield item
    
    return gen(), gen()

# request, response 디버깅
# @app.middleware("http")
# async def log_request(request: Request, call_next):
#     print("request:", (await request.body()).decode())
#     response = await call_next(request)
#     if response.body_iterator:
#         gen1, gen2 = await clone_async_iterator(response.body_iterator)
#         response.body_iterator = gen1
#         print("response:", "\n".join([item.decode() async for item in gen2]))
#     return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    for error in exc.errors():
        if isinstance(error, dict) and error.get("type", None) == "missing":
            raise MissingRequiredFieldError()
    return await request_validation_exception_handler(request, exc)
