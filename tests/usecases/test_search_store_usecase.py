import unittest

from src.clup.providers.store_provider_abc import StoreProvider
from src.clup.usecases.search_store_usecase import SearchStoreUseCase
from src.clup.entities.store import Store


class MockStoreProvider(StoreProvider):
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def add_store(self):
        raise NotImplementedError()

    def update_store(self):
        raise NotImplementedError()

    def delete_store(self):
        raise NotImplementedError()


class TestSearchStoreUsecase(unittest.TestCase):
    def setUp(self):
        self.store_provider = MockStoreProvider()
        self.u = SearchStoreUseCase(self.store_provider)

    def test_stores_with_name_is_found_in_stores(self):
        stores = self.store_provider.get_stores()
        store = Store(2, 'Esselunga', 'address')
        stores.append(store)

        stores_found = self.u.execute('Esselunga')

        self.assertEqual(len(stores_found), 1)
        self.assertTrue(store in stores_found)

    def test_all_stores_returned_on_empty_name(self):
        stores = self.store_provider.get_stores()
        store = Store(2, 'Esselunga', 'address')
        stores.append(store)

        stores_found = self.u.execute('')

        self.assertEqual(len(stores_found), 1)
        self.assertTrue(store in stores_found)

    def test_stores_found_is_empty_if_store_provider_is_empty(self):
        stores_found = self.u.execute('Conad')

        self.assertEqual(len(stores_found), 0)

    def test_stores_found_is_empty_if_name_is_not_present(self):
        stores = self.store_provider.get_stores()
        store = Store(2, 'Esselunga', 'address')
        stores.append(store)

        stores_found = self.u.execute('Conad')

        self.assertEqual(len(stores_found), 0)

    def test_search_using_substring_in_uppercase(self):
        stores = self.store_provider.get_stores()
        store = Store(2, 'Esselunga', 'address')
        stores.append(store)

        stores_found = self.u.execute('ESSE')

        self.assertEqual(len(stores_found), 1)
        self.assertTrue(store in stores_found)

    def test_search_using_substring_in_lowercase(self):
        stores = self.store_provider.get_stores()
        store = Store(2, 'Esselunga', 'address')
        stores.append(store)

        stores_found = self.u.execute('esse')

        self.assertEqual(len(stores_found), 1)
        self.assertTrue(store in stores_found)
