import unittest

from src.clup.usecases.add_store_usecase import AddStoreUseCase


class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def add_store(self, store_id):
        self.stores.append(store_id)


class TestAddStoreUseCase(unittest.TestCase):
    def test_store_is_added_to_stores(self):
        store_provider = MockStoreProvider()
        u = AddStoreUseCase(store_provider)
        store_id = 1

        u.execute(store_id)
        stores = store_provider.get_stores()
        
        self.assertTrue(store_id in stores)

    def test_adding_same_store_twice_throws_value_error(self):
        store_provider = MockStoreProvider()
        u = AddStoreUseCase(store_provider)
        store_id = 1
        u.execute(store_id)
        
        with self.assertRaises(ValueError):
            u.execute(store_id)
        
        
