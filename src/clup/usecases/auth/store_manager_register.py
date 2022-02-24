from werkzeug.security import generate_password_hash

from src.clup.entities.store_manager import StoreManager


class StoreManagerRegister:
    def __init__(self, store_manager_provider):
        self.store_manager_provider = store_manager_provider

    def execute(self, secret_key, username, password):
        if not secret_key or not username or not password:
            raise ValueError('empty fields')
        sm = self.store_manager_provider.get_store_managers()
        if username in [m.username for m in sm]:
            raise ValueError('username already in use')
        try:
            manager_id = self.store_manager_provider \
                .get_id_from_secret(secret_key)
            pw_hash = generate_password_hash(password)
            sm = StoreManager(manager_id, username, pw_hash)
            self.store_manager_provider.add_manager(sm)
        except ValueError:
            raise

        return manager_id
