class InitLanes:
    def __init__(self, lane_provider, aisle_provider, store_provider, notifier):
        self.lane_provider = lane_provider
        self.aisle_provider = aisle_provider
        self.store_provider = store_provider
        self.notifier = notifier

    def execute(self):
        for aisle in self.aisle_provider.get_aisles():
            aisle_pool = self.lane_provider.get_aisle_pool(aisle.id)
            aisle_pool.capacity = aisle.capacity
        for store in self.store_provider.get_stores():
            store_pool = self.lane_provider.get_store_pool(store.id)
            store_pool.attach(self.notifier)
