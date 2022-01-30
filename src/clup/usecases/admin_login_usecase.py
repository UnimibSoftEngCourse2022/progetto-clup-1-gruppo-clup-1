class AdminLoginUseCase:
    def __init__(self, admin_provider):
        self.admin_provider = admin_provider

    def execute(self, admin_id, password):
        for admin in self.admin_provider.get_admins():
            if admin.id == admin_id and admin.password == password:
                return True
        return False