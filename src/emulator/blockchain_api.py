import time
import typing

from pytoniq import LiteBalancer
from pytoniq_core import Cell
from pytoniq_core.tlb.config import ConfigParam34
from pytvm.transaction_emulator import BlockchainApi

from src.config import CONFIG, MAX_REQ_PER_PEER

client: "CachedLiteBalancer" = None


class CachedLiteBalancer(LiteBalancer, BlockchainApi):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}  # {address: (block, state)}
        self.last_gc_time = 0

    def get_config_cell(self):
        return self.execute_method('_get_config_cell', self.last_mc_block)

    def gc_cache(self):
        if time.time() - self.last_gc_time > 60:
            s = time.time()
            last_block = self.last_mc_block
            for address, item in list(self.cache.items()):
                if item[0].seqno < last_block.seqno - 3:
                    del self.cache[address]
            self.last_gc_time = time.time()
            self._logger.info(f'gc time: {time.time() - s}, Cache size: {len(self.cache)}')

    async def raw_get_account_state(self, address, block=None, **kwargs):
        if block is None:
            block = self.last_mc_block
        data = self.cache.get(address)
        if data is not None:
            if data[0] == block or block.seqno - data[0].seqno <= 1:
                return data[1]
        s = time.time()
        result = await super().raw_get_account_state(address, block, choose_random=True, **kwargs)
        self._logger.debug(f'get_account_state time: {time.time() - s}, address: {address}')
        if time.time() - s > 0.25:
            self._logger.info(f'get_account_state time: {time.time() - s}, address: {address}')
        self._logger.debug(f'current_req_num: {self._current_req_num}')
        if sum(self._current_req_num.values()) > 100:
            self._logger.info(f'current_req_num: {self._current_req_num}')
        self.cache[address] = (block, result)
        self.gc_cache()
        return result


async def init_client():
    global client
    client = CachedLiteBalancer.from_config(config=CONFIG, trust_level=2)
    client.max_req_per_peer = MAX_REQ_PER_PEER
    await client.start_up()


async def get_blockchain_api() -> BlockchainApi:
    if client is None:
        await init_client()
    return client


async def get_current_blockchain_config() -> typing.Tuple[Cell, ConfigParam34]:
    await get_blockchain_api()
    param = await client.get_config_params([34])
    return await client.get_config_cell(), param[34]
