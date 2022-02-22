class InitLanes:
    def __init__(self, lane_provider, aisle_provider):
        self.lane_provider = lane_provider
        self.aisle_provider = aisle_provider

    def execute(self):
        for aisle in self.aisle_provider.get_aisles():
            aisle_pool = self.lane_provider.get_aisle_pool(aisle.id)
            aisle_pool.capacity = aisle.capacity
