class GetStoreCategoriesUseCase:
    def __init__(self, aisle_provider):
        self.aisle_provider = aisle_provider

    def execute(self, store_id):
        aisles = self.aisle_provider.get_store_aisles(store_id)
        if len(aisles) == 0:
            raise ValueError("unable to find any aisle for this store_id")

        categories = [cat for a in aisles for cat in a.categories]
        return set(categories)
