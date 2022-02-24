import uuid


class CreateStoreManagerUseCase:
    def __init__(self, store_manager_provider):
        self.store_manager_provider = store_manager_provider

    def execute(self, secret_key):
        store_manager_id = str(uuid.uuid1())
        if not secret_key:
            raise ValueError("missing secret key")
        self.store_manager_provider.create_new_store_manager(store_manager_id, secret_key)

        return store_manager_id
