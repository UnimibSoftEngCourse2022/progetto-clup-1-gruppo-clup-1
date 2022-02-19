import unittest
from unittest.mock import Mock

from src.clup.entities.store import Store
from src.clup.entities.admin import Admin
from src.clup.usecases.admin_register_usecase import AdminRegisterUseCase


class MockAdminProvider:
    def __init__(self):
        self.admins = {}
        self.admin_stores = []

    def add_admin(self, admin):
        self.admins[admin.id] = admin

    def add_admin_to_store(self, admin_id, store_id):
        self.admin_stores.append((admin_id, store_id))

    def get_admins(self):
        return self.admins.values()


class MockStoreProvider:
    def __init__(self):
        self.stores = {}

    def add_store(self, store):
        self.stores[store.id] = store

    def get_stores(self):
        return self.stores.values()


class TestAdminRegisterUsecase(unittest.TestCase):
    def setUp(self):
        self.admin_pvd = MockAdminProvider()
        self.msp = MockStoreProvider()
        s1 = Store('store1', 'name1', 'Milano', 'secret1')
        s2 = Store('store2', 'name2', 'Roma', 'secret2')
        self.msp.add_store(s1)
        self.msp.add_store(s2)

        self.u = AdminRegisterUseCase(self.admin_pvd, self.msp)

    def test_add_admin_updates_admins(self):
        self.admin_pvd.add_admin = Mock()
        self.admin_pvd.add_admin_to_store = Mock()
        username = 'pippo'
        password = 'pwd'
        s_id = 'store1'

        a_id = self.u.execute(username, password, s_id, 'secret1')
        adm = Admin(a_id, username, password)

        self.admin_pvd.add_admin.assert_called_once_with(adm)
        self.admin_pvd.add_admin_to_store.assert_called_once_with(a_id, s_id)

    def test_null_or_empty_username_or_password_throws(self):
        with self.assertRaises(ValueError):
            self.u.execute(None, 'pwd', 'store1', 'secret1')

        with self.assertRaises(ValueError):
            self.u.execute('usr', None, 'store2', 'secret2')

        with self.assertRaises(ValueError):
            self.u.execute('', 'pwd', 'store1', 'secret1')

        with self.assertRaises(ValueError):
            self.u.execute('usr', '', 'store2', 'secret2')

    def test_admin_username_is_unique(self):
        self.admin_pvd.get_admins = Mock()
        existing_admin = Admin('uuid1', 'usr', 'pwd1')
        self.admin_pvd.get_admins.return_value = [existing_admin]

        with self.assertRaises(ValueError):
            self.u.execute('usr', 'pwd2', 'store2', 20)

    def test_admin_with_wrong_secret_throws(self):
        wrong_secret = 'wrong'

        with self.assertRaises(ValueError):
            self.u.execute('usr', 'pwd', 'store1', wrong_secret)

    def test_admin_linked_to_correct_store(self):
        self.admin_pvd.add_admin_to_store = Mock()
        store1_id = 'store1'
        store2_id = 'store2'

        a1_id = self.u.execute('admin1', 'pwd1', store1_id, 'secret1')
        a2_id = self.u.execute('admin2', 'pwd2', store2_id, 'secret2')

        self.admin_pvd.add_admin_to_store.assert_any_call(a1_id, store1_id)
        self.admin_pvd.add_admin_to_store.assert_any_call(a2_id, store2_id)
        self.assertEqual(self.admin_pvd.add_admin_to_store.call_count, 2)

    def test_admin_link_is_based_on_store_id_only(self):
        self.admin_pvd.add_admin = Mock()
        self.admin_pvd.add_admin_to_store = Mock()
        same_secret_as_2 = 'secret2'
        store3_id = 'store3'
        s3 = Store(store3_id, 'name3', 'Firenze', same_secret_as_2)
        self.msp.add_store(s3)
        username = 'usr'
        password = 'pwd'
        
        a_id = self.u.execute(username, password, store3_id, same_secret_as_2)
        adm = Admin(a_id, username, password)

        self.admin_pvd.add_admin.assert_called_once_with(adm)
        self.admin_pvd.add_admin_to_store.assert_called_once_with(a_id, store3_id)

    def test_register_on_unexistent_store_id_throws(self):
        with self.assertRaises(ValueError):
            self.u.execute('usr', 'pwd', 'unexistent_id', 'secret')
