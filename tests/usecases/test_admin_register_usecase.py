import unittest

from src.clup.entities.store import Store
from src.clup.usecases.admin_register_usecase import AdminRegisterUsecase


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
        self.m_a_p = MockAdminProvider()
        self.msp = MockStoreProvider()
        store1 = Store(id='store1', name='name1', address='Milano', secret=10)
        store2 = Store('store2', 'name2', 'Roma', 20)
        self.msp.add_store(store1)
        self.msp.add_store(store2)

    def test_add_admin_updates_admins(self):
        ar = AdminRegisterUsecase(self.m_a_p, self.msp)
        admin_username = 1
        admin_password = 100
        ar.execute(username=admin_username,
                   password=admin_password,
                   store_id='store1',
                   store_secret_key=10)
        is_admins_updated = len(self.m_a_p.get_admins()) != 0
        is_store_admin_updated = len(self.m_a_p.admin_stores) != 0

        self.assertTrue(is_admins_updated)
        self.assertTrue(is_store_admin_updated)

    def test_admins_contains_only_correct_elements(self):
        ar = AdminRegisterUsecase(self.m_a_p, self.msp)
        admin1_username = 1
        admin1_password = 10
        admin2_username = 2

        ar.execute(admin1_username, admin1_password, 'store1', 10)

        is_admin1_registered = admin1_username in [admin.username for admin in self.m_a_p.get_admins()]
        is_admin2_registered = admin2_username in [admin.username for admin in self.m_a_p.get_admins()]

        self.assertTrue(is_admin1_registered)
        self.assertFalse(is_admin2_registered)

    def test_null_fields_raise_exception(self):
        ar = AdminRegisterUsecase(self.m_a_p, self.msp)
        admin1_username = 1
        admin1_password = None
        admin2_username = None
        admin2_password = 20

        with self.assertRaises(ValueError):
            ar.execute(admin1_username, admin1_password, 'store1', 10)
        with self.assertRaises(ValueError):
            ar.execute(admin2_username, admin2_password, 'store2', 20)

    def test_admin_username_is_unique(self):
        ar = AdminRegisterUsecase(self.m_a_p, self.msp)
        admin1_username = 1
        admin1_password = 10
        admin2_username = 1
        admin2_password = 20

        ar.execute(admin1_username, admin1_password, 'store1', 10)
        with self.assertRaises(ValueError):
            ar.execute(admin2_username, admin2_password, 'store1', 10)

    def test_add_admin_with_wrong_secret_raise_err(self):
        ar = AdminRegisterUsecase(self.m_a_p, self.msp)
        admin1_username = 'admin1'
        admin1_password = 'password1'

        with self.assertRaises(ValueError):
            ar.execute(admin1_username, admin1_password, 'store1', 'wrong_s_k')

    def test_correct_admin_linked_to_store(self):
        ar = AdminRegisterUsecase(self.m_a_p, self.msp)
        admin1_username = 'admin1'
        admin1_password = 'password1'
        admin2_username = 'admin2'
        admin2_password = 'password2'

        admin1_id = ar.execute(admin1_username, admin1_password, 'store1', 10)
        admin2_id = ar.execute(admin2_username, admin2_password, 'store2', 20)
        first = [t for t in self.m_a_p.admin_stores if t[0] == admin1_id][0]
        second = [t for t in self.m_a_p.admin_stores if t[0] == admin2_id][0]

        self.assertTrue(first[1] == 'store1')
        self.assertTrue(second[1] == 'store2')
