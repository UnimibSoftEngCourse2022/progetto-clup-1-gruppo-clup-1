import unittest

from src.clup.usecases.store_list_usecase import StoreListUseCase


class MockStoreProvider:
    def __init__(self, stores):
        self.stores = stores

    def get_stores(self):
        return self.stores

class TestStoreListUsecase(unittest.TestCase):
    def test_stores_is_empty_if_store_list_is_empty(self):
        empty_stores = ()
        mock_store_provider = MockStoreProvider(empty_stores)
        u = StoreListUseCase(mock_store_provider)

        stores = u.execute()
        is_empty = len(stores) == 0

        self.assertTrue(is_empty)

    def test_stores_is_not_empty_if_store_list_is_not_empty(self):
        store_list = (1, 1)
        mock_store_provider = MockStoreProvider(store_list)
        u = StoreListUseCase(mock_store_provider)

        stores = u.execute()
        is_correct_length = len(stores) == 2

        self.assertTrue(is_correct_length)
