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