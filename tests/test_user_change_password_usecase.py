import unittest

from src.clup.entities.user import User
from src.clup.usecases.user_change_password_usecase import UserChangePasswordUseCase


class MockUserProvider:
    def __init__(self):
        self.users = {}

    def add_user(self, user):
        self.users[user.id] = user

    def get_users(self):
        return self.users.values()

    def get_user(self, user_id):
        return self.users[user_id]


class TestUserChangePasswordUsecase(unittest.TestCase):
    def test_change_password_set_new_password_with_correct_info(self):
        mock_user_provider = MockUserProvider()
        user = User(1, 10)
        mock_user_provider.add_user(user)
        ucp = UserChangePasswordUseCase(mock_user_provider)

        ucp.execute(user.id, user.password, 20)
        is_password_updated = 20 == user.password

        self.assertTrue(is_password_updated)

    def test_change_password_raise_exception_with_wrong_password(self):
        mock_user_provider = MockUserProvider()
        user = User(1, 10)
        mock_user_provider.add_user(user)
        ucp = UserChangePasswordUseCase(mock_user_provider)

        with self.assertRaises(ValueError):
            ucp.execute(user.id, 11, 20)

    def test_change_password_raise_exception_with_wrong_username(self):
        mock_user_provider = MockUserProvider()
        user1 = User(1, 10)
        user2 = User(2, 20)
        mock_user_provider.add_user(user1)
        mock_user_provider.add_user(user2)
        ucp = UserChangePasswordUseCase(mock_user_provider)

        with self.assertRaises(ValueError):
            ucp.execute(user2.id, user1.password, 30)

    def test_change_password_raise_value_error_with_empty_password(self):
        mock_user_provider = MockUserProvider()
        user1 = User(1, 10)
        user2 = User(2, 20)
        mock_user_provider.add_user(user1)
        mock_user_provider.add_user(user2)
        ucp = UserChangePasswordUseCase(mock_user_provider)

        with self.assertRaises(ValueError):
            ucp.execute(user1.id, user1.password, None)
        with self.assertRaises(ValueError):
            ucp.execute(user2.id, user2.password, "")