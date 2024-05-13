from fastapi import FastAPI

from . import endpoints


app = FastAPI()
app.include_router(endpoints.router)
