from collections import defaultdict

from src.clup.entities.active_pool import ActivePool
from src.clup.entities.waiting_queue import WaitingQueue
from src.clup.providers.queue_provider_abc import QueueProvider


class BasicQueueProvider(QueueProvider):
    def __init__(self):
        self.queues = defaultdict(WaitingQueue)
        self.pools = defaultdict(ActivePool)

    def get_waiting_queue(self, store_id):
        return self.queues[store_id]

    def get_active_pool(self, store_id):
        return self.pools[store_id]
