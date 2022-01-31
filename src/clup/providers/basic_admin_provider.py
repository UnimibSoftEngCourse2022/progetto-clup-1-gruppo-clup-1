class BasicAdminProvider:
    def __init__(self):
        self.admins = {}

    def get_admin(self):
        return self.admins.values()

    def add_admin(self, admin):
        if admin.id in self.admins.keys():
            raise ValueError("Admin already present")

        self.admins[admin.id] = admin

    def remove_admin(self, admin_id):
        if admin_id not in self.admins.keys():
            raise ValueError("admin-id not existing")
        del self.admins[admin_id]