class LoadStoreInfoUseCase:
    def __init__(self, store_provider, aisle_provider):
       self.store_provider = store_provider
       self.aisle_provider = aisle_provider

    def execute(self, store_id):
        stores = self.store_provider.get_stores()
        found_store = None
        for store in stores:
            if store.id == store_id:
                found_store = store

        if found_store is None:
            raise ValueError('unexistent store id')

        aisle_ids = self.aisle_provider.get_store_aisle_ids(store_id)
        aisles = self.aisle_provider.get_aisles()
        store_aisles = []
        for aisle_id in aisle_ids:
            for aisle in aisles:
                if aisle.id == aisle_id:
                    store_aisles.append(aisle)

        return {'store': found_store,
                'aisles': store_aisles}
