from src.clup.providers.abc.store_provider import StoreProvider


class MockStoreProvider(StoreProvider):
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def get_store(self, store_id):
        raise NotImplementedError()

    def add_store(self, store):
        raise NotImplementedError()

    def update_store(self, store):
        raise NotImplementedError()

    def delete_store(self, store_id):
        raise NotImplementedError()

    def get_store_from_manager_id(self, manager_id):
        raise NotImplementedError()
