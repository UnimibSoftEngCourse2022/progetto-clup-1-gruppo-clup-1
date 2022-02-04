import unittest

from src.clup.entities.admin import Admin
from src.clup.usecases.admin_register_usecase import AdminRegisterUsecase


class MockAdminProvider:
    def __init__(self):
        self.admins = {}

    def add_admin(self, admin):
        self.admins[admin.id] = admin

    def get_admins(self):
        return self.admins.values()


class TestAdminRegisterUsecase(unittest.TestCase):
    def test_add_admin_updates_admins(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        admin_username = 1
        admin_password = 10
        ar.execute(admin_username, admin_password)
        is_admins_updated = len(m_a_p.get_admins()) != 0

        self.assertTrue(is_admins_updated)

    def test_admins_contains_only_correct_elements(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        admin1_username = 1
        admin1_password = 10
        admin2_username = 2

        ar.execute(admin1_username, admin1_password)

        is_admin1_registered = admin1_username in [admin.username for admin in m_a_p.get_admins()]
        is_admin2_registered = admin2_username in [admin.username for admin in m_a_p.get_admins()]

        self.assertTrue(is_admin1_registered)
        self.assertFalse(is_admin2_registered)

    def test_null_fields_raise_exception(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        admin1_username = 1
        admin1_password = None
        admin2_username = None
        admin2_password = 20

        with self.assertRaises(ValueError):
            ar.execute(admin1_username, admin1_password)
        with self.assertRaises(ValueError):
            ar.execute(admin2_username, admin2_password)

    def test_admin_registered_store_set_to_default(self):
        admin1_username = 1
        admin1_password = 10
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)

        ar.execute(admin1_username, admin1_password)
        admin = [admin for admin in m_a_p.get_admins()][0]
        is_store_default = admin.store == 'default'

        self.assertTrue(is_store_default)

    def test_admin_username_is_unique(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        admin1_username = 1
        admin1_password = 10
        admin2_username = 1
        admin2_password = 20

        ar.execute(admin1_username, admin1_password)
        with self.assertRaises(ValueError):
            ar.execute(admin2_username, admin2_password)
