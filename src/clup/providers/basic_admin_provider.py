class BasicAdminProvider:
    def __init__(self):
        self.admin = {}

    def get_admin(self):
        return self.admin.values()

    def add_admin(self, admin):
        self.admin[admin.id] = admin

