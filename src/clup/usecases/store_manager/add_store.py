import uuid

from src.clup.entities.store import Store


class AddStore:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, name, address, manager_id='default'):
        store_id = str(uuid.uuid1())
        new_store = Store(store_id, name, address)
        stores = self.store_provider.get_stores()
        for store in stores:
            if store.name == new_store.name and \
                    store.address == new_store.address:
                raise ValueError('store already present')

        if not name:
            raise ValueError('store name is empty')

        if not address:
            raise ValueError('store address is empty')

        self.store_provider.add_store(new_store)
        self.store_provider.add_manager_to_store(store_id, manager_id)
        return new_store
