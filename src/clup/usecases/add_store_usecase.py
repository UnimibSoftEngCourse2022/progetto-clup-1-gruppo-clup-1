
class AddStoreUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, store_id):
        if store_id in self.store_provider.get_stores():
            raise ValueError('store_id already present')

        self.store_provider.add_store(store_id)
