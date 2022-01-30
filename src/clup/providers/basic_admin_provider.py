class BasicAdminProvider:
    def __init__(self):
        self.admin = {}

    def get_admin(self):
        return self.admin.values()

    def add_admin(self, admin):
        if admin.id in self.admin.keys():
            raise ValueError("Admin already present")

        self.admin[admin.id] = admin

    def remove_admin(self, admin):
        del self.admin[admin.id]
