
class StoreManagerRegisterUseCase:
    def __init__(self, store_manager_provider):
        self.store_manager_provider = store_manager_provider

    def execute(self, secret_key, username, password):
        try:
            manager_id = self.store_manager_provider \
                .get_manager_id_from_sk(secret_key)
            self.store_manager_provider.add_manager(manager_id, username, password)
        except ValueError:
            raise
