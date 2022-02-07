import uuid

from src.clup.entities.store_manager import StoreManager


class StoreManagerRegisterUseCase:
    def __init__(self, store_manager_provider, app_secret_key):
        self.store_manager_provider = store_manager_provider
        self.secret_key = app_secret_key

    def execute(self, username, password, secret_key):
        if not username or not password or not secret_key:
            raise ValueError("some fields are missing")
        if secret_key != self.secret_key:
            raise ValueError("wrong secret key")
        if username in [mg.username for mg in self.store_manager_provider.get_managers()]:
            raise ValueError("username already used")
        manager_id = uuid.uuid1()
        manager = StoreManager(manager_id, username, password)
        self.store_manager_provider.add_manager(manager)