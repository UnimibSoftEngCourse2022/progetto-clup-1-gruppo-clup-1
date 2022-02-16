import uuid

from src.clup.entities.admin import Admin


class AdminRegisterUsecase:
    def __init__(self, admin_provider, store_provider):
        self.admin_provider = admin_provider
        self.store_provider = store_provider

    def execute(self, username, password, store_id, store_secret_key):
        admin_id = str(uuid.uuid1())

        if not username or not password or not store_id or not store_secret_key:
            raise ValueError('missing fields')

        if username in [adm.username for adm in self.admin_provider.get_admins()]:
            raise ValueError('username already present')

        store_id = [store.id for store in self.store_provider.get_stores() if store.secret == store_secret_key]
        if len(store_id) != 1:
            raise ValueError("unable to find correct store for this secret key")
        store_id = store_id[0]

        admin = Admin(admin_id, username, password)
        self.admin_provider.add_admin(admin)
        self.admin_provider.add_admin_to_store(admin_id, store_id)

        return admin_id
