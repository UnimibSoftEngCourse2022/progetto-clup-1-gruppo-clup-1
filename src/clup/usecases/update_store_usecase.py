class UpdateStoreUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, store):
        stores = self.store_provider.get_stores()
        found = False
        for store_item in stores:
            if store_item.id == store.id:
                self.store_provider.update_store(store)
                found = True

        if not found:
            raise ValueError('store isnt in the stores list')

        if not store.name:
            raise ValueError('store name is empty')

        if not store.address:
            raise ValueError('store address is empty')

        if store.capacity < 0:
            raise ValueError('capacity is negative')
