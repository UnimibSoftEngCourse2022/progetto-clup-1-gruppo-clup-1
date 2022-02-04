import unittest

from src.clup.entities.category import Category
from src.clup.usecases.add_aisle_usecase import AddAisleUseCase
from src.clup.providers.basic_aisle_provider import BasicAisleProvider


class TestAddAisleUseCase(unittest.TestCase):
    def test_correct_aisle_is_added(self):
        bap = BasicAisleProvider()
        aa = AddAisleUseCase(bap)
        store_id = 'my_store'
        aisle_name = 'my_aisle'
        categories = [Category.FISH, Category.MEAT]

        aa.execute(store_id, aisle_name, categories)
        is_aisle_present = aisle_name in [aisle.name for aisle in bap.get_store_aisles(store_id)]

        self.assertTrue(is_aisle_present)

    def test_raise_except_if_not_category(self):
        bap = BasicAisleProvider()
        aa = AddAisleUseCase(bap)
        store_id = 'my_store'
        aisle_name = 'my_aisle'
        categories = [Category.FISH, Category.MEAT, 'not a category']

        with self.assertRaises(ValueError):
            aa.execute(store_id, aisle_name, categories)

    def test_aisle_aisle_added_to_correct_store(self):
        bap = BasicAisleProvider()
        aa = AddAisleUseCase(bap)
        store1_id = 'my_store'
        aisle1_name = 'my_aisle'
        categories1 = [Category.FISH, Category.MEAT]
        store2_id = 'another store'
        aisle2_name = 'another aisle'
        categories2 = [Category.FRUIT, Category.VEGETABLE]

        aa.execute(store1_id, aisle1_name, categories1)
        aa.execute(store2_id, aisle2_name, categories2)
        is_aisle1_in_store2 = aisle1_name in [aisle.name for aisle in bap.get_store_aisles(store2_id)]
        is_aisle2_in_store1 = aisle2_name in [aisle.name for aisle in bap.get_store_aisles(store1_id)]
        is_aisle1_in_store1 = aisle1_name in [aisle.name for aisle in bap.get_store_aisles(store1_id)]
        is_aisle2_in_store2 = aisle2_name in [aisle.name for aisle in bap.get_store_aisles(store2_id)]

        self.assertFalse(is_aisle1_in_store2)
        self.assertFalse(is_aisle2_in_store1)
        self.assertTrue(is_aisle2_in_store2)
        self.assertTrue(is_aisle1_in_store1)
