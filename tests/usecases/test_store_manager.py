import unittest

from src.clup.database import engine
from src.clup.providers.sqlite.sqlite_store_manager_provider import SqliteStoreManagerProvider
from src.clup.usecases.system.create_store_manager import CreateStoreManagerUseCase
from src.clup.usecases.auth.store_manager_register_usecase import StoreManagerRegisterUseCase


@unittest.skip('davide')
class TestStoreManagerCreateAndRegister(unittest.TestCase):
    def test_everything_works(self):
        ssmp = SqliteStoreManagerProvider(engine)
        csm = CreateStoreManagerUseCase(ssmp)
        secret_key = 'secret'
        manager_id = csm.execute(secret_key)
        rsm = StoreManagerRegisterUseCase(ssmp)
        rsm.execute(secret_key, 'username', 'password')
        ssmp.delete_store_manager(manager_id)

    def test_correct_parameters_set(self):
        ssmp = SqliteStoreManagerProvider(engine)
        csm = CreateStoreManagerUseCase(ssmp)
        secret_key = 'secret'
        manager_id = csm.execute(secret_key)
        rsm = StoreManagerRegisterUseCase(ssmp)
        rsm.execute(secret_key, 'username', 'password')
        manager = ssmp.get_manager(manager_id)
        ssmp.delete_store_manager(manager_id)

        self.assertTrue(manager.username == 'username')
        self.assertTrue(manager.password == 'password')
        self.assertTrue(manager.id == manager_id)
