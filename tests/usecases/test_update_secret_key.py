import unittest
from unittest.mock import create_autospec

from src.clup.entities.store import Store
from src.clup.providers.abc.store_provider import StoreProvider
from src.clup.usecases.store_manager.update_store_key import UpdateStoreKey


class TestUpdateStoreKey(unittest.TestCase):
    def setUp(self):
        self.msp = create_autospec(StoreProvider)
        self.u = UpdateStoreKey(self.msp)

    def test_everything_work_correctly(self):
        s = Store('sid', 'name', 'addr', 'secret1')
        self.msp.get_store_from_manager_id.return_value = s
        new_secret = 'new_secret'
        news = Store('sid', 'name', 'addr', new_secret)

        self.u.execute('manager_id', new_secret)

        self.msp.update_store.assert_called_once_with(news)
