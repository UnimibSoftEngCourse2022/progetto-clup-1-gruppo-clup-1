import uuid
from src.clup.entities.aisle import Aisle
from src.clup.entities.category import Category


class AddAisleUseCase:
    def __init__(self, aisle_provider):
        self.aisle_provider = aisle_provider

    def execute(self, store_id, aisle_name, categories):
        a_id = uuid.uuid1
        if not store_id or not aisle_name or not categories:
            raise ValueError("fields are missing")
        for category in categories:
            if type(category) is not Category:
                raise ValueError("wrong categories")
        aisle = Aisle(a_id, aisle_name, categories)
        try:
            self.aisle_provider.add_aisle(store_id, aisle)
        except ValueError:
            raise
