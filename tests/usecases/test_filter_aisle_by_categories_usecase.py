import unittest

from src.clup.entities.aisle import Aisle
from src.clup.entities.category import Category
from src.clup.providers.basic_aisle_provider import BasicAisleProvider
from src.clup.usecases.filter_aisle_by_categories_usecase import FilterAisleByCategoriesUseCase


class TestFilterAisleByCategories(unittest.TestCase):
    def test_correct_list_returned(self):
        bap = BasicAisleProvider()
        store_id = 'store'
        categories_wanted = [Category.FISH, Category.BEAUTY]
        fauc = FilterAisleByCategoriesUseCase(bap)
        aisle1 = Aisle(id='aisle1', name='aisle1_name', capacity=10, categories=[Category.FISH, Category.MEAT])
        aisle2 = Aisle(id='aisle2', name='aisle2_name', capacity=10, categories=[Category.VEGETABLE, Category.FRUIT])
        aisle3 = Aisle(id='aisle3', name='aisle3_name', capacity=10, categories=[Category.BEVERAGE, Category.BEAUTY])
        aisle4 = Aisle(id='aisle_of_different_store',
                       name='name',
                       capacity=100,
                       categories=categories_wanted)
        bap.add_aisle(store_id, aisle1)
        bap.add_aisle(store_id, aisle2)
        bap.add_aisle(store_id, aisle3)
        bap.add_aisle('different_store_id', aisle4)

        filtered_aisle = fauc.execute(store_id, categories_wanted)
        self.assertTrue(aisle1.id in filtered_aisle)
        self.assertTrue(aisle3.id in filtered_aisle)
        self.assertTrue(aisle4.id not in filtered_aisle)

    def test_not_repeated_aisle(self):
        bap = BasicAisleProvider()
        store_id = 'store'
        categories_wanted = [Category.FISH, Category.MEAT]
        fauc = FilterAisleByCategoriesUseCase(bap)
        aisle1 = Aisle(id='aisle1', name='aisle1_name', capacity=10, categories=[Category.FISH, Category.MEAT])
        aisle2 = Aisle(id='aisle2', name='aisle2_name', capacity=10, categories=[Category.VEGETABLE, Category.FRUIT])
        aisle3 = Aisle(id='aisle3', name='aisle3_name', capacity=10, categories=[Category.BEVERAGE, Category.BEAUTY])
        aisle4 = Aisle(id='aisle_of_different_store',
                       name='name',
                       capacity=100,
                       categories=categories_wanted)
        bap.add_aisle(store_id, aisle1)
        bap.add_aisle(store_id, aisle2)
        bap.add_aisle(store_id, aisle3)
        bap.add_aisle('different_store_id', aisle4)

        aisles = fauc.execute(store_id, categories_wanted)

        self.assertEqual(len(aisles), 1)
        self.assertTrue(aisle1.id in aisles)

    def test_correct_errors_raised(self):
        bap = BasicAisleProvider()
        store_id = 'store'
        categories_wanted = [Category.FISH, Category.MEAT]
        fauc = FilterAisleByCategoriesUseCase(bap)
        aisle1 = Aisle(id='aisle1', name='aisle1_name', capacity=10, categories=[Category.FISH, Category.MEAT])
        aisle2 = Aisle(id='aisle2', name='aisle2_name', capacity=10, categories=[Category.VEGETABLE, Category.FRUIT])
        aisle3 = Aisle(id='aisle3', name='aisle3_name', capacity=10, categories=[Category.BEVERAGE, Category.BEAUTY])
        aisle4 = Aisle(id='aisle_of_different_store',
                       name='name',
                       capacity=100,
                       categories=categories_wanted)
        bap.add_aisle(store_id, aisle1)
        bap.add_aisle(store_id, aisle2)
        bap.add_aisle(store_id, aisle3)
        bap.add_aisle('different_store_id', aisle4)

        with self.assertRaises(ValueError):
            fauc.execute('not_a_store_id', categories_wanted)
        with self.assertRaises(ValueError):
            fauc.execute(store_id, [])
        with self.assertRaises(ValueError):
            fauc.execute(store_id, [Category.BAKERY])
