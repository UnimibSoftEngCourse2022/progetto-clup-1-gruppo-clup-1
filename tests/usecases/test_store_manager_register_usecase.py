import unittest

from src.clup.usecases.store_manager_register_usecase import StoreManagerRegisterUseCase


class MockStoreManagerProvider:
    def __init__(self):
        self.store_managers = {}

    def add_manager(self, manager):
        self.store_managers[manager.id] = manager

    def get_managers(self):
        return self.store_managers.values()


class TestStoreManagerRegisterUseCase(unittest.TestCase):
    def test_manager_correctly_added(self):
        msmp = MockStoreManagerProvider()
        username = 'manager'
        password = 'password'
        secret_key = 'sk'
        smr = StoreManagerRegisterUseCase(msmp, 'sk')

        smr.execute(username, password, secret_key)
        managers = msmp.get_managers()
        manager = [mg for mg in managers if mg.username == username][0]
        is_mg_present = manager.username == username

        self.assertTrue(is_mg_present)

    def test_wrong_sk_raise_exception(self):
        msmp = MockStoreManagerProvider()
        username = 'manager'
        password = 'password'
        secret_key = 'wrong sk'
        smr = StoreManagerRegisterUseCase(msmp, 'sk')

        with self.assertRaises(ValueError):
            smr.execute(username, password, secret_key)

    def test_none_fields_raise_exception(self):
        msmp = MockStoreManagerProvider()
        username = 'manager'
        password = 'password'
        secret_key = 'sk'
        smr = StoreManagerRegisterUseCase(msmp, 'sk')

        with self.assertRaises(ValueError):
            smr.execute("", password, secret_key)

        with self.assertRaises(ValueError):
            smr.execute(username, "", secret_key)

        with self.assertRaises(ValueError):
            smr.execute(username, password, "")

    def test_already_existing_username_raise_exception(self):
        msmp = MockStoreManagerProvider()
        username = 'manager'
        password = 'password'
        secret_key = 'sk'
        smr = StoreManagerRegisterUseCase(msmp, 'sk')

        smr.execute(username, password, secret_key)
        with self.assertRaises(ValueError):
            smr.execute(username, "other pw", secret_key)
