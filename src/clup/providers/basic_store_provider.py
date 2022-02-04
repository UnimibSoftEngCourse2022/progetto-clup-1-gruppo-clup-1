from collections import defaultdict


class BasicStoreProvider:
    def __init__(self):
        self.stores = []
        self.queues = defaultdict(tuple)

    def get_stores(self):
        return self.stores

    def add_store(self, store):
        if store.id in (s.id for s in self.stores):
            raise ValueError('Store already present')

        self.stores.append(store)

    def get_queue(self, store_id):
        return self.queues[store_id]

    def add_to_queue(self, store_id, element):
        self.queues[store_id] += (element,)
