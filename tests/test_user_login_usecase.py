import unittest

from src.clup.entities.user import User
from src.clup.usecases.user_login_usecase import UserLoginUseCase


class MockUserProvider:
    def __init__(self):
        self.users = ()

    def add_user(self, user):
        users = self.users
        new_users = users + (user, )
        self.users = new_users

    def get_users(self):
        return self.users


class TestUserLoginUsecase(unittest.TestCase):
    def test_login_returns_true_when_correct_info(self):
        mock_user_provider = MockUserProvider()
        user = User(1, 10)
        mock_user_provider.users = (user,)
        ul = UserLoginUseCase(mock_user_provider)
        
        is_login_ok = ul.execute(user.id, user.password)

        self.assertTrue(is_login_ok)