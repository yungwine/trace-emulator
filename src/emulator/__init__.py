from .main import emulate
from .blockchain_api import init_client
from .transaction_emulator import init_config


async def init_emulator():
    await init_client()
    await init_config()
