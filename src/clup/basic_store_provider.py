class BasicStoreProvider:
    def __init__(self):
        self.stores = {}

    def get_stores(self):
        return self.stores.keys()
    
    def add_store(self, store_id):
        if store_id in self.stores.keys():
            raise ValueError('Store already present')

        self.stores[store_id] = []

    def get_queue(self, store_id):
        return self.stores[store_id]

    def set_queue(self, store_id, queue):
        self.stores[store_id] = queue
