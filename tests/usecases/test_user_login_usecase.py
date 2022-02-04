import unittest

from src.clup.entities.user import User
from src.clup.usecases.user_login_usecase import UserLoginUseCase


class MockUserProvider:
    def __init__(self):
        self.users = ()

    def add_user(self, user):
        users = self.users
        new_users = users + (user,)
        self.users = new_users

    def get_users(self):
        return self.users


class TestUserLoginUsecase(unittest.TestCase):
    def test_login_returns_true_when_correct_info(self):
        mock_user_provider = MockUserProvider()
        user = User(0, 1, 10)
        mock_user_provider.users = (user,)
        ul = UserLoginUseCase(mock_user_provider)

        is_login_ok = ul.execute(user.username, user.password) is not None

        self.assertTrue(is_login_ok)

    def test_login_raise_exception_if_password_or_username_not_correct(self):
        mock_user_provider = MockUserProvider()
        user = User(0, 1, 10)
        mock_user_provider.users = (user,)
        ul = UserLoginUseCase(mock_user_provider)

        with self.assertRaises(ValueError):
            ul.execute(1, 11)
        with self.assertRaises(ValueError):
            ul.execute(2, 10)

    def test_login_can_happen_with_multiple_users(self):
        mock_user_provider = MockUserProvider()
        user1 = User(0, 1, 10)
        user2 = User(5, 2, 20)
        mock_user_provider.users = (user1, user2)
        ul = UserLoginUseCase(mock_user_provider)

        is_user1_logged = ul.execute(user1.username, user1.password) == user1.id
        is_user2_logged = ul.execute(user2.username, user2.password) == user2.id

        self.assertTrue(is_user1_logged)
        self.assertTrue(is_user2_logged)
