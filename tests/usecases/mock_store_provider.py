from src.clup.providers.store_provider_abc import StoreProvider


class MockStoreProvider(StoreProvider):
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def add_store(self, store):
        raise NotImplementedError()

    def update_store(self, store):
        raise NotImplementedError()

    def delete_store(self, store_id):
        raise NotImplementedError()