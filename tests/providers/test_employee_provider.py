import unittest

from src.clup.providers.employee_provider import EmployeeProvider


class TestEmployeeProvider(unittest.TestCase):
    def test_add_manager_works_fine(self):
        store_id = "store"
        manager_id = "manager"
        ep = EmployeeProvider()

        ep.add_store_manager(store_id, manager_id)
        is_manager_added = ep.get_store_manager_id(store_id) == manager_id

        self.assertTrue(is_manager_added)

    def test_add_admin_works_fine(self):
        store_id = "store"
        admin_id = "admin"
        ep = EmployeeProvider()

        ep.add_store_admin(store_id, admin_id)
        is_admin_added = ep.get_store_admins_id(store_id) == [admin_id]

        self.assertTrue(is_admin_added)

    def test_add_manager_froze_with_username_already_present(self):
        store_id = "store"
        manager_id = "manager"
        ep = EmployeeProvider()
        ep.add_store_manager(store_id, manager_id)

        with self.assertRaises(ValueError):
            ep.add_store_manager(store_id, "new manager")

    def test_multiple_admins_for_same_store_permitted(self):
        store_id = "store"
        diff_store_id = "diff_store"
        admin1_id = "admin1"
        admin2_id = "admin2"
        admin3_id = "admin3"
        admin4_id = "admin4"
        ep = EmployeeProvider()

        ep.add_store_admin(store_id, admin1_id)
        ep.add_store_admin(store_id, admin2_id)
        ep.add_store_admin(diff_store_id, admin3_id)
        ep.add_store_admin(diff_store_id, admin4_id)

        admins_store = ep.get_store_admins_id(store_id)
        admins_diff_store = ep.get_store_admins_id(diff_store_id)
        is_admins_store_correct = admin1_id in admins_store and admin2_id in admins_store
        is_admins_diff_store_correct = admin3_id in admins_diff_store and admin4_id in admins_diff_store

        self.assertTrue(is_admins_store_correct)
        self.assertTrue(is_admins_diff_store_correct)

    def test_get_store_id_from_manager_id_returns_correct_val(self):
        store1_id = "store1"
        manager1_id = "manager1"
        store2_id = "store2"
        manager2_id = "manager2"
        ep = EmployeeProvider()
        ep.add_store_manager(store1_id, manager1_id)
        ep.add_store_manager(store2_id, manager2_id)

        store1_from_ep = ep.get_store_id_from_manager_id(manager1_id)
        store2_from_ep = ep.get_store_id_from_manager_id(manager2_id)
        is_store1_correct = store1_from_ep == store1_id
        is_store2_correct = store2_from_ep == store2_id

        self.assertTrue(is_store1_correct)
        self.assertTrue(is_store2_correct)

        with self.assertRaises(ValueError):
            ep.get_store_id_from_manager_id("not existing manager")

    def test_get_store_id_from_admin_works_fine(self):
        store_id = "store"
        diff_store_id = "diff_store"
        admin1_id = "admin1"
        admin2_id = "admin2"
        admin3_id = "admin3"
        admin4_id = "admin4"
        ep = EmployeeProvider()
        ep.add_store_admin(store_id, admin1_id)
        ep.add_store_admin(store_id, admin2_id)
        ep.add_store_admin(diff_store_id, admin3_id)
        ep.add_store_admin(diff_store_id, admin4_id)

        store_from_ep_correct = ep.get_store_id_from_admin_id(admin1_id) == ep.get_store_id_from_admin_id(
            admin2_id) == store_id
        diff_store_from_ep_correct = ep.get_store_id_from_admin_id(admin3_id) == ep.get_store_id_from_admin_id(
            admin4_id) == diff_store_id

        self.assertTrue(store_from_ep_correct)
        self.assertTrue(diff_store_from_ep_correct)
        with self.assertRaises(ValueError):
            ep.get_store_id_from_admin_id("not a valid id")
