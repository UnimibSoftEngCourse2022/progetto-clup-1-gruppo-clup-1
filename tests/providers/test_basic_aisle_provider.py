import unittest
from src.clup.providers.basic_aisle_provider import BasicAisleProvider


class TestBasicAisleProvider(unittest.TestCase):
    def test_basic_aisle_provider_set_empty(self):
        bap = BasicAisleProvider()
        is_empty = bap.aisles == {}

        self.assertTrue(is_empty)

    def test_bap_update_aisles_with_correct_info(self):
        bap = BasicAisleProvider()
        store_id = 0
        aisle = 1

        bap.add_aisle(store_id, aisle)
        aisles = bap.get_store_aisles(store_id)
        is_aisle_present = aisle in aisles

        self.assertTrue(is_aisle_present)

    def test_bap_update_if_store_already_present(self):
        bap = BasicAisleProvider()
        store_id = 0
        aisle1 = 1
        aisle2 = 2

        bap.add_aisle(store_id, aisle1)
        bap.add_aisle(store_id, aisle2)
        is_store_aisles_correct = bap.get_store_aisles(store_id) == (1, 2)

        self.assertTrue(is_store_aisles_correct)

    def test_bap_raise_exception_if_store_id_not_exist_on_get(self):
        bap = BasicAisleProvider()
        store_id = 1

        with self.assertRaises(ValueError):
            bap.get_store_aisles(store_id)

    def test_bap_raise_exception_if_aisle_already_present(self):
        bap = BasicAisleProvider()
        store_id = 1
        aisle = 1

        bap.add_aisle(store_id, aisle)

        with self.assertRaises(ValueError):
            bap.add_aisle(store_id, aisle)

    def test_bap_has_different_fields_for_different_stores(self):
        bap = BasicAisleProvider()
        store1_id = 1
        aisle1 = 1
        store2_id = 2
        aisle2 = 2

        bap.add_aisle(store1_id, aisle1)
        bap.add_aisle(store2_id, aisle2)
        is_aisle1_present = aisle1 in bap.aisles[store1_id]
        is_aisle2_present = aisle2 in bap.aisles[store2_id]
        is_aisle1_present_in_store2 = aisle1 in bap.aisles[store2_id]
        is_aisle2_present_in_store1 = aisle2 in bap.aisles[store1_id]

        self.assertTrue(is_aisle1_present)
        self.assertTrue(is_aisle2_present)
        self.assertFalse(is_aisle1_present_in_store2)
        self.assertFalse(is_aisle2_present_in_store1)
