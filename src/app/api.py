from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from . import endpoints


app = FastAPI(title='Trace emulator', description='Trace emulator for TON Blockchain.')
app.include_router(endpoints.router)
Instrumentator(
    env_var_name="ENABLE_METRICS"
).instrument(app).expose(app)
