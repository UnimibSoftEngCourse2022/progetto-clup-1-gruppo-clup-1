import unittest

from src.clup.entities.store import Store
from src.clup.entities.store_manager import StoreManager
from src.clup.usecases.update_store_key_usecase import UpdateStoreKeyUseCase


class MockStoreProvider:
    def __init__(self):
        self.stores = {}
        self.store_and_managers = {}

    def get_store_manager_by_username(self, username):
        for manager in self.store_and_managers.values():
            if manager.username == username:
                return manager

    def get_store_from_manager_id(self, manager_id):
        result = None
        for store_id, manager in self.store_and_managers.items():
            if manager.id == manager_id:
                result = store_id
        return self.stores[result]

    def update_store(self, new_store):
        self.stores[new_store.id] = new_store

    def add_store(self, store):
        self.stores[store.id] = store

    def add_store_manager(self, store_id, manager):
        self.store_and_managers[store_id] = manager


class TestUpdateStoreKey(unittest.TestCase):
    def setUp(self):
        self.msp = MockStoreProvider()
        store1 = Store(id='store1id',
                       name='store1name',
                       address='address1')
        store2 = Store(id='store2id',
                       name='store2name',
                       address='address2')
        self.msp.add_store(store1)
        self.msp.add_store(store2)
        manager1 = StoreManager(id='manager1id',
                                username='username1',
                                password='password1')
        manager2 = StoreManager(id='manager2id',
                                username='username2',
                                password='password2')
        self.msp.add_store_manager('store1id', manager1)
        self.msp.add_store_manager('store2_id', manager2)

    def test_everything_work_correctly(self):
        usk = UpdateStoreKeyUseCase(self.msp)
        usk.execute('username1', 'password1', 100)

        secret_key = self.msp.stores['store1id'].secret

        self.assertTrue(secret_key == 100)

    def test_wrong_password_raise_error(self):
        usk = UpdateStoreKeyUseCase(self.msp)

        with self.assertRaises(ValueError):
            usk.execute('username1', 'wrong_pw', 100)

    def test_only_correct_key_updated(self):
        usk = UpdateStoreKeyUseCase(self.msp)

        usk.execute('username1', 'password1', 100)
        secret_key = self.msp.stores['store2id'].secret

        self.assertTrue(secret_key == '0')
