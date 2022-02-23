class LoadStoreManagerUseCase:
    def __init__(self, store_manager_provider):
        self.store_manager_provider = store_manager_provider

    def execute(self, manager_id):
        try:
            sm = self.store_manager_provider.get_manager(manager_id)
            return sm
        except ValueError:
            raise
