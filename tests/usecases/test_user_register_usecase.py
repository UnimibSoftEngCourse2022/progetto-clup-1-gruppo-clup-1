import unittest
from unittest.mock import Mock

from werkzeug.security import check_password_hash

from src.clup.usecases.auth.user_register_usecase import UserRegisterUsecase


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
    def setUp(self):
        self.user_provider = MockUserProvider()
        self.u = UserRegisterUsecase(self.user_provider)

    def test_user_in_mock_user_provider(self):
        self.user_provider.add_user = Mock()
        username = 'pippo'
        password = 'pwd'

        u_id = self.u.execute(username, password)

        self.user_provider.add_user.assert_called_once()
        args = self.user_provider.add_user.call_args.args
        created_user = args[0]
        self.assertEqual(created_user.id, u_id)
        self.assertEqual(created_user.username, username)
        self.assertTrue(check_password_hash(created_user.password_hash, password))

    def test_users_contains_only_correct_user(self):
        user_id1 = 1
        password1 = 'pwd1'
        user_id2 = 2

        self.u.execute(user_id1, password1)
        is_user1_present = self.user_provider.get_user(user_id1).username == user_id1
        is_user2_present = self.user_provider.get_user(user_id2) is not None

        self.assertTrue(is_user1_present)
        self.assertFalse(is_user2_present)

    def test_users_can_contain_multiple_users(self):
        user_id1 = 1
        password1 = 'pwd1'
        user_id2 = 2
        password2 = 'pwd2'

        self.u.execute(user_id1, password1)
        self.u.execute(user_id2, password2)
        is_user1_present = self.user_provider.get_user(user_id1).username == user_id1
        is_user2_present = self.user_provider.get_user(user_id2).username == user_id2

        self.assertTrue(is_user1_present)
        self.assertTrue(is_user2_present)

    def test_null_field_raise_error(self):
        with self.assertRaises(ValueError):
            self.u.execute('usr', None)
        with self.assertRaises(ValueError):
            self.u.execute(None, 'pwd')

    def test_add_same_user_twice_raise_error(self):
        username = 'usr'
        password = 'pwd'

        self.u.execute(username, password)
        with self.assertRaises(ValueError):
            self.u.execute(username, password)

    def test_empty_string_raise_error(self):
        with self.assertRaises(ValueError):
            self.u.execute("", 'pwd1')
        with self.assertRaises(ValueError):
            self.u.execute('usr1', "")
