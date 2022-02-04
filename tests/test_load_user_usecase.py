import unittest

from src.clup.entities.user import User
from src.clup.usecases.load_user_data_usecase import LoadUserDataUseCase


class MockUserProvider:
    def __init__(self):
        self.users = {}

    def get_users(self):
        return self.users.values()

    def get_user(self, user_id):
        return self.users[user_id]


class TestLoadUserDataUsecase(unittest.TestCase):
    def test_load_user_return_user(self):
        mup = MockUserProvider()
        user = User(1, 'tizio', 'caio')
        mup.users[1] = user
        lu = LoadUserDataUseCase(mup)

        is_user_returned = lu.execute(1) == user

        self.assertTrue(is_user_returned)

    def test_raise_excp_if_user_id_not_present(self):
        mup = MockUserProvider()
        user = User(1, 'tizio', 'caio')
        mup.users[1] = user
        lu = LoadUserDataUseCase(mup)

        with self.assertRaises(ValueError):
            lu.execute(2)
