import uuid

from src.clup.entities.admin import Admin


class AdminRegisterUseCase:
    def __init__(self, admin_provider, store_provider):
        self.admin_provider = admin_provider
        self.store_provider = store_provider

    def execute(self, username, password, store_name, store_address, store_secret):
        if not username or not password or not store_address or not store_name:
            raise ValueError('missing fields')

        if username in [a.username for a in self.admin_provider.get_admins()]:
            raise ValueError('username already present')

        store_id = self.store_provider.get_store_id_from_name_and_address(store_name, store_address)
        found_store = None
        for store in self.store_provider.get_stores():
            if store.id == store_id:
                found_store = store

        if found_store is None:
            raise ValueError('store not found')

        if found_store.secret != store_secret:
            raise ValueError('invalid secret')

        admin_id = str(uuid.uuid1())
        admin = Admin(admin_id, username, password)

        self.admin_provider.add_admin(admin)
        self.admin_provider.add_admin_to_store(admin_id, store_id)

        return admin_id
