class EnableAdminUseCase:
    def __init__(self, admin_provider, store_provider):
        self.admin_provider = admin_provider
        self.store_provider = store_provider

    def execute(self, admin_id, store_id, secret):
        if store_id not in [store.id for store in self.store_provider.get_stores()]:
            raise ValueError("store not existing")
        store = [store for store in self.store_provider.get_stores() if store.id == store_id][0]
        if store.secret== secret:
            if admin_id not in [admin.id for admin in self.admin_provider.get_admins()]:
                raise ValueError("admin not existing")
            self.admin_provider.get_admin(admin_id).store = store_id
        else:
            raise ValueError("wrong secret_key")
