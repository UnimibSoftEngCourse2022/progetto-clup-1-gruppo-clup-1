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

    def test_remove_correct_admin(self):
        bap = BasicAdminProvider()
        admin1 = Admin(1, 12)
        admin2 = Admin(2, 30)

        bap.add_admin(admin2)
        bap.add_admin(admin1)
        bap.remove_admin(admin1.id)
        is_admin1_in_bap = admin1 in bap.get_admin()
        is_admin2_in_bap = admin2 in bap.get_admin()

        self.assertFalse(is_admin1_in_bap)
        self.assertTrue(is_admin2_in_bap)

    def test_add_admin_twice_froze(self):
        bap = BasicAdminProvider()
        admin1 = Admin(1, 12)
        admin2 = Admin(1, 15)

        bap.add_admin(admin1)

        with self.assertRaises(ValueError):
            bap.add_admin(admin2)

    def test_remove_admin_not_present_froze(self):
        bap = BasicAdminProvider()
        admin = Admin(1, 10)
        bap.add_admin(admin)

        with self.assertRaises(ValueError):
            bap.remove_admin(2)
            




