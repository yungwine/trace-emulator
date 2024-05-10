import time

from pytoniq_core import Slice
from pytvm.transaction_emulator import TransactionEmulator

from src.emulator.blockchain_api import get_current_blockchain_config

BC_CONFIG = None
BC_CONFIG_TIME = 0
VALIDATE_FOR = 2**16


class MyTransactionEmulator(TransactionEmulator):
    """
    Transaction Emulator without deserializing `Transaction` Tl-B object.
    """

    @staticmethod
    def _process_tr_emulation_result(result: dict):
        from pytoniq_core.tlb.transaction import Transaction, OutList
        from pytoniq_core.tlb.account import ShardAccount
        if result['success']:
            result['actions'] = OutList.deserialize(Slice.one_from_boc(result['actions'])) if result['actions'] else []
            result['shard_account'] = ShardAccount.deserialize(Slice.one_from_boc(result['shard_account']))
            result['transaction'] = Transaction.deserialize(Slice.one_from_boc(result['transaction']))
            result['transaction_boc'] = result['transaction']
        return result


async def init_config():
    global BC_CONFIG, BC_CONFIG_TIME
    BC_CONFIG, param = await get_current_blockchain_config()
    BC_CONFIG_TIME = param.cur_validators.utime_since


async def get_trans_emulator() -> TransactionEmulator:
    emulator = TransactionEmulator()
    if BC_CONFIG is None or BC_CONFIG_TIME + VALIDATE_FOR + 60 < time.time():  # it's time to update config!
        await init_config()
    emulator.set_unixtime(int(time.time()))
    emulator.set_config(BC_CONFIG)
    return emulator
