import unittest

from src.clup.usecases.add_store_usecase import AddStoreUseCase


class MockStoreProvider:
    def __init__(self):
        self.stores = []

    def get_stores(self):
        return self.stores

    def add_store(self, store):
        self.stores.append(store)


class TestAddStoreUseCase(unittest.TestCase):
    def test_store_is_added_to_stores(self):
        store_provider = MockStoreProvider()
        u = AddStoreUseCase(store_provider)
        name = "store"
        address = "address"
        capacity = 1

        store = u.execute(name, address, capacity)
        stores = store_provider.get_stores()

        self.assertTrue(store in stores)

    def test_adding_same_store_twice_throws_value_error(self):
        store_provider = MockStoreProvider()
        u = AddStoreUseCase(store_provider)
        name = "store"
        address = "address"
        capacity = 1

        u.execute(name, address, capacity)

        with self.assertRaises(ValueError):
            u.execute(name, address, 5)

    def test_name_field_of_a_store_is_empty(self):
        store_provider = MockStoreProvider()
        u = AddStoreUseCase(store_provider)
        name = ""
        address = "address"
        capacity = 1

        with self.assertRaises(ValueError):
            u.execute(name, address, capacity)

    def test_address_field_of_a_store_is_empty(self):
        store_provider = MockStoreProvider()
        u = AddStoreUseCase(store_provider)
        name = "store"
        address = ""
        capacity = 1

        with self.assertRaises(ValueError):
            u.execute(name, address, capacity)

    def test_capacity_not_negative(self):
        store_provider = MockStoreProvider()
        u = AddStoreUseCase(store_provider)
        name = "store"
        address = "address"
        capacity = -1

        with self.assertRaises(ValueError):
            u.execute(name, address, capacity)
