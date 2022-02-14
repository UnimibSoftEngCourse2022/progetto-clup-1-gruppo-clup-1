import unittest

from src.clup.usecases.search_store_usecase import SearchStoreUseCase
from src.clup.entities.store import Store

class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores



class TestSearchStoreUsecase(unittest.TestCase):
    def test_store_is_founded_stores(self):
        store_provider = MockStoreProvider()
        u = SearchStoreUseCase(store_provider)
        store = Store(1, 'name', 'address')
        store_provider.stores.append(store)