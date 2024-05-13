from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from . import endpoints


app = FastAPI()
app.include_router(endpoints.router)

FastAPICache.init(InMemoryBackend())
