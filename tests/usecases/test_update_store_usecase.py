import unittest

from src.clup.entities.store import Store
from src.clup.usecases.update_store_usecase import UpdateStoreUseCase


class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def update_store(self, store):
        for store_item in self.stores:
            if store_item.id == store.id:
                store_item.name = store.name
                store_item.address = store.address
                store_item.capacity = store.capacity


class TestUpdateStoreUseCase(unittest.TestCase):
    def test_store_is_updated_in_stores(self):
        store_provider = MockStoreProvider()
        store = Store(1, 'name', 'address', 1)
        store_provider.stores.append(store)
        u = UpdateStoreUseCase(store_provider)

        u.execute(store)
        stores = store_provider.get_stores()

        self.assertTrue(store in stores)

    def test_update_on_unexisting_id_throws(self):
        store_provider = MockStoreProvider()
        u = UpdateStoreUseCase(store_provider)
        store = Store(1, 'name', 'address', 1)

        with self.assertRaises(ValueError):
            u.execute(store)
