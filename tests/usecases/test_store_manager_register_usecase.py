import unittest
from unittest.mock import Mock

from werkzeug.security import check_password_hash

from src.clup.entities.store_manager import StoreManager
from src.clup.providers.abc.store_manager_provider_abc \
    import StoreManagerProvider
from src.clup.usecases.auth.store_manager_register_usecase import StoreManagerRegisterUseCase


class MockStoreManagerProvider(StoreManagerProvider):
    def __init__(self):
        self.store_managers = {}
        self.store_manager_stores = []

    def get_store_managers(self):
        return self.store_managers.values()

    def create_new_store_manager(self, sm_id, secret):
        raise NotImplementedError()

    def get_id_from_secret(self, secret):
        raise NotImplementedError()

    def add_manager(self, id, usr, pwd):
        raise NotImplementedError()

    def delete_store_manager(self, sm_id, secret):
        raise NotImplementedError()

    def get_manager(self, sm_id, secret):
        raise NotImplementedError()

    def update(self, sm_id, secret):
        raise NotImplementedError()


class TestStoreManagerRegisterUsecase(unittest.TestCase):
    def setUp(self):
        self.store_manager_pvd = MockStoreManagerProvider()
        self.u = StoreManagerRegisterUseCase(self.store_manager_pvd)

    def test_add_store_manager_updates_store_managers(self):
        self.store_manager_pvd.add_manager = Mock()
        self.store_manager_pvd.get_id_from_secret = Mock()
        self.store_manager_pvd.get_id_from_secret.return_value = 'manager_id'
        username = 'pippo'
        password = 'pwd'

        sm_id = self.u.execute('secret', username, password)

        self.store_manager_pvd.get_id_from_secret.assert_called_once_with('secret')
        self.store_manager_pvd.add_manager.assert_called_once()
        args = self.store_manager_pvd.add_manager.call_args.args
        created_store_manager = args[0]
        self.assertEqual(created_store_manager.id, sm_id)
        self.assertEqual(created_store_manager.username, username)
        self.assertTrue(check_password_hash(created_store_manager.password_hash, password))

    def test_null_or_empty_username_or_password_throws(self):
        with self.assertRaises(ValueError):
            self.u.execute(None, 'usr', 'pwd')

        with self.assertRaises(ValueError):
            self.u.execute('secret', None, 'pwd')

        with self.assertRaises(ValueError):
            self.u.execute('secret', 'usr', None)

    def test_store_manager_username_is_unique(self):
        self.store_manager_pvd.get_store_managers = Mock()
        existing_store_manager = StoreManager('sm1_id', 'usr', 'pwd1')
        self.store_manager_pvd.get_store_managers.return_value = [existing_store_manager]
        self.store_manager_pvd.get_id_from_secret = Mock()
        self.store_manager_pvd.get_id_from_secret.return_value = 'sm2_id'
        self.store_manager_pvd.add_manager = Mock()

        with self.assertRaises(ValueError):
            self.u.execute('secret', 'usr', 'pwd2')
            self.store_manager_pvd.add_manager.assert_not_called()

    def test_store_manager_with_wrong_secret_throws(self):
        self.store_manager_pvd.get_id_from_secret = Mock()
        self.store_manager_pvd.get_id_from_secret.side_effect = ValueError()
        wrong_secret = 'wrong'

        with self.assertRaises(ValueError):
            self.u.execute(wrong_secret, 'usr', 'pwd')
