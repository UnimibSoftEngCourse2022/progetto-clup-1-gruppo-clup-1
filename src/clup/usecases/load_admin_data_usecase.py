class LoadAdminDataUseCase:
    def __init__(self, admin_provider):
        self.admin_provider = admin_provider

    def execute(self, admin_id):
        if admin_id not in [user.id for user in self.admin_provider.get_admins()]:
            raise ValueError("user_id non valido")
        if not admin_id:
            raise ValueError("user_id non valido")
        if self.admin_provider.get_admin(admin_id) is None:
            raise ValueError("None!!")
        return self.admin_provider.get_admin(admin_id)
