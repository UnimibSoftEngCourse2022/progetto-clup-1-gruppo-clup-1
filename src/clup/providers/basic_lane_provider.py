from collections import defaultdict

from src.clup.entities.active_pool import ActivePool
from src.clup.entities.store_active_pool import StoreActivePool
from src.clup.entities.waiting_queue import WaitingQueue
from src.clup.providers.lane_provider_abc import LaneProvider


class BasicLaneProvider(LaneProvider):
    def __init__(self):
        self.queues = defaultdict(WaitingQueue)
        self.pools = defaultdict(ActivePool)
        self.store_pools = defaultdict(StoreActivePool)

    def get_waiting_queue(self, aisle_id):
        return self.queues[aisle_id]

    def get_aisle_pool(self, aisle_id):
        return self.pools[aisle_id]

    def get_store_pool(self, store_id):
        return self.store_pools[store_id]
