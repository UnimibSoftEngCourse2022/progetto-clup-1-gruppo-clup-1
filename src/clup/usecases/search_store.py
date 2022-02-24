class SearchStore:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, string):
        stores = self.store_provider.get_stores()
        new_found = [s for s in stores if string.lower() in s.name.lower()]
        return new_found
