from collections import defaultdict

from src.clup.entities.aisle_pool import AislePool
from src.clup.entities.store_pool import StorePool
from src.clup.entities.waiting_queue import WaitingQueue
from src.clup.providers.abc.lane_provider_abc import LaneProvider


class MockLaneProvider(LaneProvider):
    def __init__(self):
        self.queues = defaultdict(WaitingQueue)
        self.pools = defaultdict(AislePool)
        self.store_pools = defaultdict(StorePool)

    def get_waiting_queue(self, aisle_id):
        return self.queues[aisle_id]

    def get_aisle_pool(self, aisle_id):
        return self.pools[aisle_id]

    def get_store_pool(self, store_id):
        return self.store_pools[store_id]
