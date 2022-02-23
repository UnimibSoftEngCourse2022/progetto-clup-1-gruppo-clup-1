import unittest

from src.clup.entities.aisle import Aisle
from src.clup.entities.store import Store
from src.clup.usecases.load_store_info_usecase \
    import LoadStoreInfoUseCase
from tests.usecases.mock_aisle_provider import MockAisleProvider
from tests.usecases.mock_store_provider import MockStoreProvider


class TestLoadStoreInfoUseCase(unittest.TestCase):
    def setUp(self):
        self.store_provider = MockStoreProvider()
        self.aisle_provider = MockAisleProvider()
        self.u = LoadStoreInfoUseCase(self.store_provider, self.aisle_provider)

    def test_should_throw_on_uexistent_store_id(self):
        with self.assertRaises(ValueError):
            self.u.execute('unexistent_id')

    def test_should_return_store_with_id(self):
        store = Store('store_id', 'name', 'address')
        self.store_provider.stores.append(store)

        info = self.u.execute('store_id')
        info_store = info['store']

        self.assertEqual(info_store.id, store.id)
        self.assertEqual(info_store.name, store.name)
        self.assertEqual(info_store.address, store.address)

    def test_should_return_store_with_id_only(self):
        store1 = Store('store1_id', 'name1', 'address1')
        store2 = Store('store2_id', 'name2', 'address2')
        self.store_provider.stores.append(store1)
        self.store_provider.stores.append(store2)

        info = self.u.execute('store1_id')
        info_store = info['store']

        self.assertEqual(info_store.id, store1.id)
        self.assertEqual(info_store.name, store1.name)
        self.assertEqual(info_store.address, store1.address)

    def test_should_return_aisles_for_given_store(self):
        store = Store('store_id', 'name', 'address')
        self.store_provider.stores.append(store)
        aisle1 = Aisle('aisle1_id', 'name1', 'cat1')
        aisle2 = Aisle('aisle2_id', 'name2', 'cat2')
        self.aisle_provider.aisles['store_id'] = [aisle1, aisle2]

        info = self.u.execute('store_id')
        info_aisles = info['aisles']

        self.assertEqual(info_aisles, [aisle1, aisle2])
