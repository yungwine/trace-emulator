import asyncio
import typing
from fastapi import APIRouter
from fastapi_cache.decorator import cache
from pydantic import BaseModel


from src.emulator import emulate, init_emulator

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
@cache(expire=5)
async def emulate_endp(
        request_body: EmulateBody,
):
    try:
        res = await asyncio.wait_for(await emulate(request_body.message), timeout=10)
        return res
    except asyncio.TimeoutError:
        return {'ok': False, 'message': 'timeout', 'result': {}}
    except Exception as e:
        return {'ok': False, 'message': str(e), 'result': {}}


@router.on_event("startup")
async def startup():
    await init_emulator()
