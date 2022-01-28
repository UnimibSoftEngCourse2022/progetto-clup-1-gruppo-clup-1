class StoreListUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self):
        return self.store_provider.get_stores()