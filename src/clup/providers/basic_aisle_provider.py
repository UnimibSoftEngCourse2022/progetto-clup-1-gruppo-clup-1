from src.clup.providers.aisle_provider_abc import AisleProvider


class BasicAisleProvider(AisleProvider):
    def __init__(self):
        self.aisles = {}

    def get_store_aisles(self, store_id):
        if store_id not in self.aisles.keys():
            raise ValueError('wrong store_id')
        return self.aisles[store_id]

    def add_aisle(self, store_id, aisle):
        if store_id not in self.aisles.keys():
            self.aisles[store_id] = (aisle,)
        else:
            old_aisles = self.aisles[store_id]
            if aisle in old_aisles:
                raise ValueError('aisle already present')
            new_aisles = old_aisles + (aisle,)
            self.aisles[store_id] = new_aisles
