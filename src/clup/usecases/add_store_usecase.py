import uuid

from src.clup.entities.store import Store


class AddStoreUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, name, address, capacity):
        store_id = str(uuid.uuid1())
        new_store = Store(store_id, name, address, capacity)
        stores = self.store_provider.get_stores()
        for store in stores:
            if store.name == new_store.name and \
               store.address == new_store.address:
                raise ValueError('store alredy present')

        if not name:
            raise ValueError('store name is empty')

        if not address:
            raise ValueError('store address is empty')

        if capacity < 0:
            raise ValueError('capacity is negative')

        self.store_provider.add_store(new_store)
        return new_store
