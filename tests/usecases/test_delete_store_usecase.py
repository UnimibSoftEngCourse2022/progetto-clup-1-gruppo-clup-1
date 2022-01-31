import unittest
from src.clup.usecases.delete_store_usecase import DeleteStoreUseCase
from src.clup.entities.store import Store


class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def delete_store(self, store_id):
        for store in self.stores:
            if store.id == store_id:
                to_remove = store
        self.stores.remove(to_remove)


class TestDeleteStoreUseCase(unittest.TestCase):
    def test_store_is_deleted_to_stores(self):
        store_provider = MockStoreProvider()
        u = DeleteStoreUseCase(store_provider)
        store = Store(1, 'name', 'address', 1)
        store_provider.stores.append(store)

        old_stores = store_provider.get_stores()
        updated_stores = u.execute(store.id)

        self.assertEqual(old_stores, updated_stores)

    def test_delete_on_unexisting_id_throws(self):
        store_provider = MockStoreProvider()
        u = DeleteStoreUseCase(store_provider)
        store = Store(1, 'name', 'address', 1)

        with self.assertRaises(ValueError):
            u.execute(store)
