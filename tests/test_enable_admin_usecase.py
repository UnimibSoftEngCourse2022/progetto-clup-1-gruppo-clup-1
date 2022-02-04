import unittest

from src.clup.entities.admin import Admin
from src.clup.entities.store import Store
from src.clup.usecases.enable_admin_usecase import EnableAdminUseCase


class MockAdminProvider:
    def __init__(self):
        self.admins = {}

    def add_admin(self, admin):
        self.admins[admin.id] = admin

    def get_admins(self):
        return self.admins.values()

    def get_admin(self, admin_id):
        return self.admins[admin_id]


class MockStoreProvider:
    def __init__(self):
        self.stores = {}

    def get_stores(self):
        return self.stores.values()


class TestEnableAdminUsecase(unittest.TestCase):
    def test_admin_corrected_updated_after_activation(self):
        m_a_p = MockAdminProvider()
        msp = MockStoreProvider()
        ea = EnableAdminUseCase(m_a_p, msp)
        admin = Admin('id', 'u_n', 'password')
        store = Store('store_id', 'pippo', 'pluto')
        m_a_p.admins[admin.id] = admin
        msp.stores[store.id] = store

        ea.execute(admin.id, store.id, store.secret_key)
        is_admin_activate = admin.store == store.id

        self.assertTrue(is_admin_activate)

    def test_wrong_secret_key_raise_value_error(self):
        m_a_p = MockAdminProvider()
        msp = MockStoreProvider()
        ea = EnableAdminUseCase(m_a_p, msp)
        admin = Admin('id', 'u_n', 'password')
        store = Store('store_id', 'pippo', 'pluto')
        m_a_p.admins[admin.id] = admin
        msp.stores[store.id] = store

        with self.assertRaises(ValueError):
            ea.execute(admin.id, store.id, 'wrong_secret_key')

    def test_not_existing_admin_or_store_id_raise_value_error(self):
        m_a_p = MockAdminProvider()
        msp = MockStoreProvider()
        ea = EnableAdminUseCase(m_a_p, msp)
        admin = Admin('id', 'u_n', 'password')
        store = Store('store_id', 'pippo', 'pluto')
        m_a_p.admins[admin.id] = admin
        msp.stores[store.id] = store

        with self.assertRaises(ValueError):
            ea.execute('wrong user_id', store.id, store.secret_key)

        with self.assertRaises(ValueError):
            ea.execute(admin.id, 'wrong store_id', store.secret_key)
