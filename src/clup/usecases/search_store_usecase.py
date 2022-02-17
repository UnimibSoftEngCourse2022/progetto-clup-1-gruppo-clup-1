class SearchStoreUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, store_name):
        stores = self.store_provider.get_stores()
        found = False
        for store_item in stores:
            if store_name.lower() in store_item.name.lower():
                found = True
                return self.store_provider.get_founded_stores(store_item)

        if not found:
            raise ValueError('store isnt in the stores list')