import unittest

from src.clup.entities.aisle import Aisle
from src.clup.entities.store import Store
from src.clup.usecases.get_store_categories import GetStoreCategories


class MockAisleProvider:
    def __init__(self):
        self.aisles = {}
        self.stores = {}

    def add_aisle(self, store_id, aisle):
        if store_id not in self.aisles.keys():
            self.aisles[store_id] = [aisle]
        else:
            self.aisles[store_id].append(aisle)

    def add_store(self, store):
        self.stores[store.id] = store

    def get_store_aisles(self, store_id):
        if store_id not in self.aisles.keys():
            return []
        return self.aisles[store_id]


class TestGetStoreCategoriesUseCase(unittest.TestCase):
    def setUp(self):
        self.maip = MockAisleProvider()
        self.maip.add_store(Store(id='store1_id',
                                  name='store1_name',
                                  address='milano'))
        self.maip.add_store(Store(id='store2_id',
                                  name='store2_name',
                                  address='roma'))
        self.maip.add_aisle('store1_id',
                            aisle=Aisle(id='aisle11_id',
                                        name='aisle11_name',
                                        categories=[1, 2, 3]))
        self.maip.add_aisle('store1_id',
                            aisle=Aisle(id='aisle12_id',
                                        name='aisle12_name',
                                        categories=[3, 4]))
        self.maip.add_aisle('store2_id',
                            aisle=Aisle(id='aisle21_id',
                                        name='aisle21_name',
                                        categories=[4, 5, 6]))
        self.maip.add_aisle('store2_id',
                            aisle=Aisle(id='aisle22_id',
                                        name='aisle22_name',
                                        categories=[5, 6, 7]))

    def test_return_category_list(self):
        gsc = GetStoreCategories(self.maip)
        cat_list = gsc.execute('store1_id')

        self.assertTrue(type(cat_list) == list)

    def test_correct_categories_added(self):
        gsc = GetStoreCategories(self.maip)

        cat_list = gsc.execute('store1_id')

        self.assertTrue(1 in cat_list)
        self.assertTrue(4 in cat_list)
        self.assertTrue(7 not in cat_list)
        self.assertTrue(5 not in cat_list)

    def test_not_repeated_element(self):
        gsc = GetStoreCategories(self.maip)

        cat_list = gsc.execute('store2_id')

        self.assertTrue(len(cat_list) == 4)

    def test_raised_err_if_cannot_find_aisles(self):
        gsc = GetStoreCategories(self.maip)

        with self.assertRaises(ValueError):
            gsc.execute('wrong_store_id')
