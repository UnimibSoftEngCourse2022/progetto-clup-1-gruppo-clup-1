import unittest
from unittest.mock import create_autospec

from tests.usecases.mock_store_provider import MockStoreProvider
from tests.usecases.mock_aisle_provider import MockAisleProvider
from tests.usecases.mock_lane_provider import MockLaneProvider

from src.clup.entities.aisle import Aisle
from src.clup.entities.store import Store
from src.clup.providers.admin_provider_abc import AdminProvider
from src.clup.usecases.load_admin_store_info_usecase \
    import LoadAdminStoreInfoUseCase


class TestLoadAdminStoreInfoUseCase(unittest.TestCase):
    def setUp(self):
        self.admin_provider = create_autospec(AdminProvider)
        self.store_provider = MockStoreProvider()
        self.aisle_provider = MockAisleProvider()
        self.lane_provider = MockLaneProvider()
        self.u = LoadAdminStoreInfoUseCase(self.store_provider, 
            self.aisle_provider, self.lane_provider, self.admin_provider)

    def test_correct_store_is_loaded(self):
        store = Store('store_id', 'name', 'address')
        self.store_provider.stores.append(store)
        self.admin_provider.get_store_id.return_value = 'store_id'

        info = self.u.execute('admin_id')
        info_store = info['store']

        self.assertEqual(info_store, store)

    def test_correct_aisles_are_loaded(self):
        store = Store('store_id', 'name', 'address')
        self.store_provider.stores.append(store)
        aisle1 = Aisle('aisle1_id', 'aisle1', 'category1', 10)
        aisle2 = Aisle('aisle2_id', 'aisle2', 'category2', 20)
        self.aisle_provider.aisles['store_id'] = [aisle1, aisle2]
        self.admin_provider.get_store_id.return_value = 'store_id'

        info = self.u.execute('admin_id')
        info_aisles = info['aisles']

        self.assertEqual(info_aisles, [aisle1, aisle2])


    def test_correct_store_capacity_calculated(self):
        store = Store('store_id', 'name', 'address')
        self.store_provider.stores.append(store)
        aisle1 = Aisle('aisle1_id', 'aisle1', 'category1', 10)
        aisle2 = Aisle('aisle2_id', 'aisle2', 'category2', 20)
        self.aisle_provider.aisles['store_id'] = [aisle1, aisle2]
        self.admin_provider.get_store_id.return_value = 'store_id'

        info = self.u.execute('admin_id')
        info_capacity = info['capacity']

        self.assertEqual(info_capacity, 30)
