from src.clup.providers.aisle_provider_abc import AisleProvider


class BasicAisleProvider(AisleProvider):
    def __init__(self):
        self.aisles = {}

    def get_aisles(self):
        raise UnimplementedError()

    def get_store_aisles(self, store_id):
        if store_id not in self.aisles.keys():
            raise ValueError('wrong store_id')
        return self.aisles[store_id]

    def get_store_aisle_ids(self, store_id):
        if store_id not in self.aisles.keys():
            raise ValueError("wrong store_id")
        return [aisle.id for aisle in self.aisles[store_id]]

    def get_aisle(self, aisle_id):
        for aisles_list in self.aisles.values():
            for aisle in aisles_list:
                if aisle.id == aisle_id:
                    return aisle
        raise ValueError("aisle_id not existing")

    def add_aisle(self, store_id, aisle):
        if store_id not in self.aisles.keys():
            self.aisles[store_id] = (aisle,)
        else:
            old_aisles = self.aisles[store_id]
            if aisle in old_aisles:
                raise ValueError('aisle already present')
            new_aisles = old_aisles + (aisle,)
            self.aisles[store_id] = new_aisles
