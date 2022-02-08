class EmployeeProvider:
    def __init__(self):
        self.store_managers = {}
        self.store_admins = {}

    def add_store_manager(self, store_id, manager_id):
        if store_id in self.store_managers.keys():
            raise ValueError("store manager already present for this store")
        self.store_managers[store_id] = manager_id

    # TODO update_store_manager(self, store_id, new_manager_id)

    def add_store_admin(self, store_id, admin_id):
        if store_id in self.store_admins.keys():
            self.store_admins[store_id].append(admin_id)
        else:
            self.store_admins[store_id] = [admin_id]

    def get_store_manager_id(self, store_id):
        if store_id not in self.store_managers.keys():
            raise ValueError("store not existing")
        return self.store_managers[store_id]

    def get_store_admins_id(self, store_id):
        if store_id not in self.store_admins.keys():
            raise ValueError("store not existing")
        return self.store_admins[store_id]

    def get_store_id_from_manager_id(self, manager_id):
        for store_id, mg_id in self.store_managers.items():
            if mg_id == manager_id:
                return store_id
        raise ValueError("manager_id not present")

    def get_store_id_from_admin_id(self, admin_id):
        for store_id, admin_list in self.store_admins.items(  ):
            if admin_id in admin_list:
                return store_id
        raise ValueError("admin_id not present")
