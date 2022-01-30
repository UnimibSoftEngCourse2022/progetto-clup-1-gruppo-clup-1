import unittest

from src.clup.entities.user import User
from src.clup.providers.basic_user_provider import BasicUserProvider


class TestBasicStoreProvider(unittest.TestCase):
    def test_is_empty_after_init(self):
        bup = BasicUserProvider()

        users = bup.get_users()
        is_empty = len(users) == 0

        self.assertTrue(is_empty)

    def test_only_correct_user_added(self):
        bup = BasicUserProvider()
        user1 = User(1, 10)
        user2 = User(2, 20)
        bup.add_users(user1)

        is_user1_added = user1 in bup.get_users()
        is_user2_added = user2 in bup.get_users()

        self.assertTrue(is_user1_added)
        self.assertFalse(is_user2_added)