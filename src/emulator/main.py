import time
import logging

from pytvm.transaction_emulator import TraceEmulator, TraceResult
from pytoniq_core import MessageAny, Slice

from .blockchain_api import get_blockchain_api
from .transaction_emulator import get_trans_emulator


logging.getLogger('LiteClient').disabled = True
logger = logging.getLogger(__name__)


def replace_trs_to_bocs(result: TraceResult):
    if result['transaction']:
        result['transaction'] = result['transaction'].cell.to_boc().hex()
    for child in result['children']:
        replace_trs_to_bocs(child)


async def emulate(message):
    api = await get_blockchain_api()
    transaction_emulator = await get_trans_emulator()
    trace_emulator = TraceEmulator(api, transaction_emulator)
    result = {
        'result': {},
        'ok': True,
        'message': ''
    }
    try:
        s = time.time()
        res = await trace_emulator.emulate(MessageAny.deserialize(Slice.one_from_boc(message)))
        replace_trs_to_bocs(res)
        logger.info(f'Emulation finished in {time.time() - s} seconds')
        result['result'] = dict(res) | {'block': trace_emulator.block.to_dict()}
    except Exception as e:
        logger.info(f'Emulation failed: {e}')
        result['ok'] = False
        result['message'] = str(e)
    return result
