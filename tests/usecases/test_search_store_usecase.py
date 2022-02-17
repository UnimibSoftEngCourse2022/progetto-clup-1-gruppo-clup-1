import unittest

from src.clup.usecases.search_store_usecase import SearchStoreUseCase
from src.clup.entities.store import Store

class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def get_founded_stores(self, stor):
        stores_founded = []
        for store in self.stores:
            if store.name == stor.name:
                stores_founded.append(store)
        return stores_founded


class TestSearchStoreUsecase(unittest.TestCase):
    def setUp(self):
        self.store_provider = MockStoreProvider()
        self.u = SearchStoreUseCase(self.store_provider)
        self.store = Store(1, 'Esselunga', 'address')
        self.store_provider.stores.append(self.store)

    def test_stores_is_founded_in_stores(self):
        stores = self.store_provider.get_stores()
        store = Store(2, 'Esselunga', 'address')
        stores.append(store)

        stores_founded = self.u.execute(self.store.name)
        
        self.assertCountEqual(stores_founded, stores)

    def test_store_is_founded_in_stores(self):
        stores = self.store_provider.get_stores()
        
        stores_founded = self.u.execute(self.store.name)

        self.assertCountEqual(stores_founded, stores)

    def test_stores_founded_is_empty_if_input_store_name_is_not_in_stores(self):
        store = Store(1, 'Conad', 'address')
        with self.assertRaises(ValueError):
            self.u.execute(store.name)
        self.assertTrue(self.store in self.store_provider.get_stores())

    def test_search_substring_uppercase(self):
        stores = self.store_provider.get_stores()
        stores_founded = self.u.execute('ESSE')

        self.assertCountEqual(stores_founded, stores)

    def test_search_lowercase(self):
        stores = self.store_provider.get_stores()
        stores_founded = self.u.execute('esselunga')

        self.assertCountEqual(stores_founded, stores)

    def test_search_substring_uppercase(self):
        stores = self.store_provider.get_stores()
        stores_founded = self.u.execute('ESSELUNGA')

        self.assertCountEqual(stores_founded, stores)