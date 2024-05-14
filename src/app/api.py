from fastapi import FastAPI

from . import endpoints


app = FastAPI(title='Trace emulator', description='Trace emulator for TON Blockchain.')
app.include_router(endpoints.router)
