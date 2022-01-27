class BasicStoreProvider:
    def __init__(self):
        self.stores = []
        self.queue = []

    def get_stores(self):
        return self.stores
    
    def add_store(self, store_id):
        if store_id in self.stores:
            raise ValueError('Store already present')

        self.stores.append(store_id)

    def get_queue(self, store_id):
        return self.queue

    def set_queue(self, store_id, queue):
        self.queue = queue
