import unittest

from src.clup.entities.user import User
from src.clup.entities.admin import Admin
from src.clup.usecases.generic_login_usecase import GenericLoginUsecase


class MockUserProvider:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.id] = user

    def get_users(self):
        return self.users.values()


class MockAdminProvider:
    def __init__(self):
        self.admins = {}

    def add_admin(self, admin):
        self.admins[admin.id]=admin

    def get_admins(self):
        return self.admins.values()


class TestGenericLoginUsecase(unittest.TestCase):
    def test_generic_login_works_with_user(self):
        mock_user_provider = MockUserProvider()
        mock_admin_provider = MockAdminProvider()
        user = User(0, 1, 10)
        mock_user_provider.add_user(user)
        gl = GenericLoginUsecase(mock_admin_provider, mock_user_provider)

        _, logged_type = gl.execute(user.username, user.password)
        is_user_logged = logged_type == 'user'

        self.assertTrue(is_user_logged)

    def test_generic_login_works_with_admin(self):
        mock_user_provider = MockUserProvider()
        mock_admin_provider = MockAdminProvider()
        user = User(0, 1, 10)
        admin = Admin(1, 2, 10)
        mock_user_provider.add_user(user)
        mock_admin_provider.add_admin(admin)
        gl = GenericLoginUsecase(mock_admin_provider, mock_user_provider)
        _, logged_type = gl.execute(admin.username, admin.password)
        is_admin_logged = logged_type == 'admin'

        self.assertTrue(is_admin_logged)

    def test_login_with_wrong_credentials_raise_exception(self):
        mock_user_provider = MockUserProvider()
        mock_admin_provider = MockAdminProvider()
        user = User(0, 1, 10)
        admin = Admin(2, 3, 10)
        mock_user_provider.add_user(user)
        mock_admin_provider.add_admin(admin)
        gl = GenericLoginUsecase(mock_admin_provider, mock_user_provider)

        with self.assertRaises(ValueError):
            gl.execute(user.id, admin.password)
        with self.assertRaises(ValueError):
            gl.execute(admin.id, user.password)