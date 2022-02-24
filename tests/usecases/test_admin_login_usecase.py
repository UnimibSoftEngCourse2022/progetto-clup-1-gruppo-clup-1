import unittest

from src.clup.entities.admin import Admin
from src.clup.usecases.auth.admin_login_usecase import AdminLoginUseCase


class MockAdminProvider:
    def __init__(self):
        self.admins = {}

    def add_admin(self, admin):
        self.admins[admin.id] = admin

    def get_admins(self):
        return self.admins.values()

    def get_admin(self, admin_id):
        return self.admins[admin_id]


@unittest.skip('Unused')
class TestAdminLoginUsecase(unittest.TestCase):
    def test_admin_login_only_if_admin_already_registered(self):
        m_a_p = MockAdminProvider()
        admin1 = Admin(0, 1, 10)
        m_a_p.admins[admin1.id] = admin1
        al = AdminLoginUseCase(m_a_p)

        is_admin1_logged_in = al.execute(admin1.username, admin1.password) == admin1.id

        self.assertTrue(is_admin1_logged_in)

    def test_wrong_password_raise_exception(self):
        m_a_p = MockAdminProvider()
        admin1 = Admin(0, 1, 10)
        m_a_p.admins[admin1.id] = admin1
        al = AdminLoginUseCase(m_a_p)

        with self.assertRaises(ValueError):
            al.execute(admin1.username, 20)

    def test_wrong_id_raise_exception(self):
        m_a_p = MockAdminProvider()
        admin1 = Admin(0, 1, 10)
        m_a_p.admins[admin1.id] = admin1
        al = AdminLoginUseCase(m_a_p)

        with self.assertRaises(ValueError):
            al.execute(2, admin1.password)
