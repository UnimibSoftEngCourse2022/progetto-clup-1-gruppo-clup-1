class FilterAisleByCategoriesUseCase:
    def __init__(self, aisle_provider):
        self.aisle_provider = aisle_provider

    def execute(self, store_id, categories):
        if not categories:
            raise ValueError("no categories received")

        aisles = self.aisle_provider.get_store_aisles(store_id)

        if len(aisles) == 0:
            raise ValueError("couldn't find any aisle for this store")

        filtered_aisle_ids = []
        for category in categories:
            found = False
            for aisle in aisles:
                if category in aisle.categories:
                    filtered_aisle_ids.append(aisle.id)
                    found = True

            if not found:
                raise ValueError(f"couldn't find {category} for this store")

        return set(filtered_aisle_ids)
