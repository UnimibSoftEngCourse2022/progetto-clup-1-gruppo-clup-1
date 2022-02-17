from src.clup.entities.store import Store


class UpdateStoreKeyUseCase:
    def __init__(self, store_provider):
        self.store_provider = store_provider

    def execute(self, manager_username, manager_password, new_key):
        store_manager = self.store_provider.get_store_manager_by_username(manager_username)

        if store_manager.password != manager_password:
            raise ValueError("incorrect password")

        store = self.store_provider.get_store_from_manager_id(store_manager.id)
        new_store = Store(
            id=store.id,
            name=store.name,
            address=store.address,
            secret=new_key
        )
        self.store_provider.update_store(new_store)