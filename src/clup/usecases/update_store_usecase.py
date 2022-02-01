class UpdateStoreUseCase:
    def __init__(self, store_provider, queue_provider):
        self.store_provider = store_provider
        self.queue_provider = queue_provider

    def execute(self, store, capacity):
        if not store.name:
            raise ValueError('store name is empty')

        if not store.address:
            raise ValueError('store address is empty')

        if capacity < 0:
            raise ValueError('capacity is negative')

        stores = self.store_provider.get_stores()
        found = False
        for store_item in stores:
            if store_item.id == store.id:
                self.store_provider.update_store(store)
                pool = self.queue_provider.get_active_pool(store_item.id)
                pool.capacity = capacity
                found = True

        if not found:
            raise ValueError('store isnt in the stores list')
