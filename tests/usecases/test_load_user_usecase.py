import unittest

from src.clup.entities.user import User
from src.clup.usecases.user.load_user_usecase import LoadUserUseCase


class MockUserProvider:
    def __init__(self):
        self.users = []

    def get_users(self):
        return self.users


class TestLoadUserDataUsecase(unittest.TestCase):
    def setUp(self):
        self.user_provider = MockUserProvider()
        self.u = LoadUserUseCase(self.user_provider)

    def test_user_is_returned(self):
        u = User('1', 'tizio', 'caio')
        self.user_provider.users.append(u)

        user = self.u.execute('1')

        self.assertEqual(user.id, '1')
        self.assertEqual(user.username, 'tizio')
        self.assertEqual(user.password_hash, 'caio')

    def test_unexistent_user_id_throws(self):
        with self.assertRaises(ValueError):
            self.u.execute('1')

    def test_user_with_id_is_returned(self):
        u1 = User('1', 'tizio', 'caio')
        u2 = User('2', 'pluto', 'paperino')
        self.user_provider.users.append(u1)
        self.user_provider.users.append(u2)

        user = self.u.execute('2')

        self.assertEqual(user.id, '2')
        self.assertEqual(user.username, 'pluto')
        self.assertEqual(user.password_hash, 'paperino')
