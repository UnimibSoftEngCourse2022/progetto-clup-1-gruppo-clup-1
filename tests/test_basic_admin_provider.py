import unittest

from src.clup.entities.admin import Admin
from src.clup.providers.basic_admin_provider import BasicAdminProvider


class TestBasicStoreProvider(unittest.TestCase):
    def test_is_empy_after_init(self):
        bap = BasicAdminProvider()

        admin = bap.get_admin()
        is_empty = len(admin) == 0

        self.assertTrue(is_empty)

    def test_only_correct_admin_added(self):
        bap = BasicAdminProvider()
        admin1 = Admin(1, 12)
        admin2 = Admin(2, 20)
        bap.add_admin(admin1)

        is_admin1_added = admin1 in bap.get_admin()
        is_admin2_added = admin2 in bap.get_admin()

        self.assertTrue(is_admin1_added)
        self.assertFalse(is_admin2_added)

