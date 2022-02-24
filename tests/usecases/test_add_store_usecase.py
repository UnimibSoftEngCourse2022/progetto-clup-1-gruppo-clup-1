import unittest

from src.clup.usecases.store_manager.add_store_usecase import AddStoreUseCase
from tests.usecases.mock_lane_provider import MockLaneProvider


class MockStoreProvider:
    def __init__(self):
        self.stores = []
        self.store_and_manager = []

    def get_stores(self):
        return self.stores

    def add_store(self, store):
        self.stores.append(store)

    def add_manager_to_store(self, store_id, manager_id):
        self.store_and_manager.append((store_id, manager_id))


class TestAddStoreUseCase(unittest.TestCase):
    def setUp(self):
        self.queue_provider = MockLaneProvider()
        self.store_provider = MockStoreProvider()
        self.u = AddStoreUseCase(self.store_provider)

    def test_store_is_added_to_stores(self):
        name = 'store'
        address = 'address'

        store = self.u.execute(name, address)
        stores = self.store_provider.get_stores()

        self.assertTrue(store in stores)

    def test_adding_same_store_twice_throws_value_error(self):
        name = 'store'
        address = 'address'

        self.u.execute(name, address)

        with self.assertRaises(ValueError):
            self.u.execute(name, address)

    def test_name_field_of_a_store_is_empty(self):
        name = ''
        address = 'address'

        with self.assertRaises(ValueError):
            self.u.execute(name, address)

    def test_address_field_of_a_store_is_empty(self):
        name = 'store'
        address = ''

        with self.assertRaises(ValueError):
            self.u.execute(name, address)

    def test_manager_id_added_to_new_Store(self):
        store_name = 'store'
        address = 'milano'
        manager = 'manager'

        ns = self.u.execute(store_name, address, manager)
        ssm = self.store_provider.store_and_manager[0]

        self.assertTrue(manager in ssm)
        self.assertTrue(ns.id in ssm)
