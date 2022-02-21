from collections import defaultdict

from src.clup.providers.aisle_provider_abc import AisleProvider


class MockAisleProvider(AisleProvider):
    def __init__(self):
        self.aisles = defaultdict(list)

    def get_aisles(self):
        return [a
                for store_aisles in self.aisles.values()
                for a in store_aisles]

    def get_aisle(self, aisle_id):
        return [a
                for store_aisles in self.aisles.values()
                for a in store_aisles
                if a.id == aisle_id][0]

    def get_store_aisle_ids(self, store_id):
        return [a.id for a in self.aisles[store_id]]

    def get_store_aisles(self, store_id):
        return [a for a in self.aisles[store_id]]

    def add_aisle(self, store_id, aisle):
        raise NotImplementedError()
