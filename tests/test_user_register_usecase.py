import unittest

from src.clup.entities.user import User
from src.clup.usecases.user_register_usecase import UserRegisterUsecase


class MockUserProvider:
    def __init__(self):
        self.users = ()

    def add_user(self, user):
        users = self.users
        new_users = users + (user, )
        self.users = new_users

    def get_users(self):
        return self.users


class TestUserRegisterUsecase(unittest.TestCase):
    def test_user_in_mock_user_provider(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user_id = 1
        password = 10
        user = User(user_id, password)

        ur.execute(user)
        is_user_present = user in mock_user_provider.get_users()

        self.assertTrue(is_user_present)

    def test_users_contains_only_correct_user(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user_id1 = 1
        password1 = 10
        user_id2 = 2
        password2 = 20
        user1 = User(user_id1, password1)
        user2 = User(user_id2, password2)

        ur.execute(user1)
        is_user1_present = user1 in mock_user_provider.get_users()
        is_user2_present = user2 in mock_user_provider.get_users()

        self.assertTrue(is_user1_present)
        self.assertFalse(is_user2_present)

    def test_users_can_contain_multiple_users(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user_id1 = 1
        password1 = 10
        user_id2 = 2
        password2 = 20
        user1 = User(user_id1, password1)
        user2 = User(user_id2, password2)

        ur.execute(user1)
        ur.execute(user2)
        is_user1_present = user1 in mock_user_provider.get_users()
        is_user2_present = user2 in mock_user_provider.get_users()

        self.assertTrue(is_user1_present)
        self.assertTrue(is_user2_present)

    def test_null_field_raise_error(self):
        user1 = User(1, None)
        user2 = User(None, 1)
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        with self.assertRaises(ValueError):
            ur.execute(user1)
        with self.assertRaises(ValueError):
            ur.execute(user2)

    def test_add_same_user_twice_raise_error(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user_id1 = 1
        password1 = 10
        user1 = User(user_id1, password1)

        ur.execute(user1)
        with self.assertRaises(ValueError):
            ur.execute(user1)

    def test_empty_string_raise_error(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user1 = User("", 10)
        user2 = User(1, "")

        with self.assertRaises(ValueError):
            ur.execute(user1)
        with self.assertRaises(ValueError):
            ur.execute(user2)


