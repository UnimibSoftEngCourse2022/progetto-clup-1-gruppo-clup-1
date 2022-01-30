import unittest

from src.clup.entities.admin import Admin
from src.clup.usecases.admin_register_usecase import AdminRegisterUsecase


class MockAdminProvider:
    def __init__(self):
        self.admins = ()

    def add_admin(self, admin):
        admins = self.admins
        new_admins = admins + (admin, )
        self.admins = new_admins

    def get_admins(self):
        return self.admins

class TestAdminRegisterUsecase(unittest.TestCase):
    def test_add_admin_updates_admins(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        admin = Admin(1, 10)

        ar.execute(admin)
        is_admins_updated = len(m_a_p.get_admins()) != 0

        self.assertTrue(is_admins_updated)

    def test_admins_contains_only_correct_elements(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        admin1 = Admin(1, 10)
        admin2 = Admin(2, 20)

        ar.execute(admin1)
        is_admin1_registered = admin1 in m_a_p.get_admins()
        is_admin2_registered = admin2 in m_a_p.get_admins()

        self.assertTrue(is_admin1_registered)
        self.assertFalse(is_admin2_registered)

    def test_null_fields_raise_exception(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        admin1 = Admin(1, None)
        admin2 = Admin(None, 20)

        with self.assertRaises(ValueError):
            ar.execute(admin1)
        with self.assertRaises(ValueError):
            ar.execute(admin2)

    def test_admin_register_raise_exception_with_anything_not_Admin(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        not_an_admin = None

        with self.assertRaises(ValueError):
            ar.execute(not_an_admin)

    def test_admin_id_is_unique(self):
        m_a_p = MockAdminProvider()
        ar = AdminRegisterUsecase(m_a_p)
        admin1 = Admin(1, 10)
        admin2 = Admin(1, 20)

        ar.execute(admin1)
        with self.assertRaises(ValueError):
            ar.execute(admin2)