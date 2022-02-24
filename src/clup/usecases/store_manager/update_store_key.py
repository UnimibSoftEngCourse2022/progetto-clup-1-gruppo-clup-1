from src.clup.entities.store import Store


class UpdateStoreKey:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, store_manager_id, new_key):
        store = self.store_provider.get_store_from_manager_id(store_manager_id)

        new_store = Store(
            id=store.id,
            name=store.name,
            address=store.address,
            secret=new_key
        )

        self.store_provider.update_store(new_store)
