import time

from pytoniq_core import Slice
from pytvm.transaction_emulator import TransactionEmulator

from src.emulator.blockchain_api import get_current_blockchain_config

BC_CONFIG = None
BC_CONFIG_TIME = 0


async def init_config():
    global BC_CONFIG, BC_CONFIG_TIME
    BC_CONFIG, param = await get_current_blockchain_config()
    BC_CONFIG_TIME = param.cur_validators.utime_until


async def get_trans_emulator() -> TransactionEmulator:
    emulator = TransactionEmulator()
    if BC_CONFIG is None or BC_CONFIG_TIME + 60 < time.time():  # it's time to update config!
        await init_config()
    emulator.set_unixtime(int(time.time()))
    emulator.set_config(BC_CONFIG)
    return emulator
