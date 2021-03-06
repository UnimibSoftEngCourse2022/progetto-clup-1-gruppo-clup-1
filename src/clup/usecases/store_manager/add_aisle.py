import uuid

from src.clup.entities.aisle import Aisle
from src.clup.entities.category import Category


class AddAisle:
    def __init__(self, aisle_provider, lane_provider):
        self.aisle_provider = aisle_provider
        self.lane_provider = lane_provider

    def execute(self, store_id, aisle_name, categories, capacity=5):
        a_id = str(uuid.uuid1())

        if not store_id or not aisle_name or not categories:
            raise ValueError("fields are missing")

        if capacity <= 0:
            raise ValueError("negative capacity")

        for category in categories:
            if type(category) is not Category:
                raise ValueError("wrong categories")

        aisle = Aisle(a_id, aisle_name, categories, capacity)
        try:
            self.aisle_provider.add_aisle(store_id, aisle)
            active_pool = self.lane_provider.get_aisle_pool(a_id)
            active_pool.capacity = capacity
            return a_id
        except ValueError:
            raise
