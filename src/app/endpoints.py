import asyncio
import logging
import typing
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pydantic import BaseModel


from src.emulator import emulate, init_emulator
from ..config import LOGGING, EMULATION_CACHE_SEC, MEMCACHED_HOST, MEMCACHED_PORT

router = APIRouter()


class EmulateBody(BaseModel):
    message: str


class EmulatorResult(BaseModel):
    result: dict
    ok: bool
    message: typing.Optional[str]


@router.get("/test")
async def test():
    return {'ok': True}


@router.post("/emulate", response_model=EmulatorResult)
@cache(expire=EMULATION_CACHE_SEC)
async def emulate_endp(
        request_body: EmulateBody,
):
    try:
        res = await asyncio.wait_for(emulate(request_body.message), timeout=10)
        return res
    except asyncio.TimeoutError:
        return {'ok': False, 'message': 'timeout', 'result': {}}
    except Exception as e:
        return {'ok': False, 'message': str(e), 'result': {}}


@router.on_event("startup")
async def startup():
    logging.basicConfig(level=LOGGING)
    await init_emulator()

    from fastapi_cache import FastAPICache
    from fastapi_cache.backends.memcached import MemcachedBackend

    from aiomcache import Client

    client = Client(MEMCACHED_HOST, MEMCACHED_PORT)
    FastAPICache.init(MemcachedBackend(client))
