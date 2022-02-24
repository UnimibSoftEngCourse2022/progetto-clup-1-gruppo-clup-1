class LoadAdminStoreInfoUseCase:
    def __init__(self, store_provider, aisle_provider,
                 lane_provider, admin_provider):
        self.store_provider = store_provider
        self.aisle_provider = aisle_provider
        self.lane_provider = lane_provider
        self.admin_provider = admin_provider

    def execute(self, admin_id):
        info = {}
        store_id = self.admin_provider.get_store_id(admin_id)
        found_store = None
        for store in self.store_provider.get_stores():
            if store.id == store_id:
                found_store = store

        aisle_ids = self.aisle_provider.get_store_aisle_ids(store_id)
        aisles = self.aisle_provider.get_aisles()
        store_aisles = []
        for aisle_id in aisle_ids:
            for aisle in aisles:
                if aisle.id == aisle_id:
                    store_aisles.append(aisle)

        info['store'] = found_store
        info['aisles'] = store_aisles
        info['capacity'] = sum(a.capacity for a in store_aisles)
        info['enabled'] = len(self.lane_provider.get_store_pool(store_id).enabled)
        info['current_people'] = len(self.lane_provider.get_store_pool(store_id).to_free)
        return info
