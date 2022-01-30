import unittest

from src.clup.entities.admin import Admin
from src.clup.usecases.admin_login_usecase import AdminLoginUseCase


class MockAdminProvider:
    def __init__(self):
        self.admins = ()

    def add_admin(self, admin):
        admins = self.admins
        new_admins = admins + (admin, )
        self.admins = new_admins

    def get_admins(self):
        return self.admins


class TestAdminLoginUsecase(unittest.TestCase):
    def test_admin_login_only_if_admin_already_registered(self):
        m_a_p = MockAdminProvider()
        admin1 = Admin(1, 10)
        admin2 = Admin(2, 20)
        m_a_p.admins = (admin1, )
        al = AdminLoginUseCase(m_a_p)

        is_admin1_logged_in = al.execute(admin1.id, admin1.password)
        # is_admin2_logged_in = al.execute(admin2.id, admin2.password)

        self.assertTrue(is_admin1_logged_in)
        # self.assertFalse(is_admin2_logged_in)

    def test_wrong_password_raise_exception(self):
        m_a_p = MockAdminProvider()
        admin1 = Admin(1, 10)
        m_a_p.admins = (admin1,)
        al = AdminLoginUseCase(m_a_p)

        with self.assertRaises(ValueError):
            al.execute(admin1.id, 20)

    def test_wrong_id_raise_exception(self):
        m_a_p = MockAdminProvider()
        admin1 = Admin(1, 10)
        m_a_p.admins = (admin1,)
        al = AdminLoginUseCase(m_a_p)

        with self.assertRaises(ValueError):
            al.execute(2, admin1.password)
