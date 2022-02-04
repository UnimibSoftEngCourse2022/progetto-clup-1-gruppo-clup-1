import unittest

from src.clup.usecases.user_register_usecase import UserRegisterUsecase


class MockUserProvider:
    def __init__(self):
        self.users = ()

    def add_user(self, user):
        users = self.users
        new_users = users + (user,)
        self.users = new_users

    def get_users(self):
        return self.users

    def get_user(self, user_name):
        for user in self.users:
            if user_name == user.username:
                return user
        return None


class TestUserRegisterUsecase(unittest.TestCase):
    def test_user_in_mock_user_provider(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user_id = 1
        password = 10

        ur.execute(user_id, password)
        is_user_present = len(mock_user_provider.get_users()) == 1

        self.assertTrue(is_user_present)

    def test_users_contains_only_correct_user(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user_id1 = 1
        password1 = 10
        user_id2 = 2
        password2 = 20

        ur.execute(user_id1, password1)
        is_user1_present = mock_user_provider.get_user(user_id1).username == user_id1
        is_user2_present = mock_user_provider.get_user(user_id2) != None

        self.assertTrue(is_user1_present)
        self.assertFalse(is_user2_present)

    def test_users_can_contain_multiple_users(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user_id1 = 1
        password1 = 10
        user_id2 = 2
        password2 = 20

        ur.execute(user_id1, password1)
        ur.execute(user_id2, password2)
        is_user1_present = mock_user_provider.get_user(user_id1).username == user_id1
        is_user2_present = mock_user_provider.get_user(user_id2).username == user_id2

        self.assertTrue(is_user1_present)
        self.assertTrue(is_user2_present)

    def test_null_field_raise_error(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        with self.assertRaises(ValueError):
            ur.execute(1, None)
        with self.assertRaises(ValueError):
            ur.execute(None, 1)

    def test_add_same_user_twice_raise_error(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)
        user_id1 = 1
        password1 = 10

        ur.execute(user_id1, password1)
        with self.assertRaises(ValueError):
            ur.execute(user_id1, password1)

    def test_empty_string_raise_error(self):
        mock_user_provider = MockUserProvider()
        ur = UserRegisterUsecase(mock_user_provider)

        with self.assertRaises(ValueError):
            ur.execute("", 10)
        with self.assertRaises(ValueError):
            ur.execute(1, "")
