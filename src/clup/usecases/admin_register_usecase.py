from src.clup.entities.admin import Admin


class AdminRegisterUsecase:
    def __init__(self, admin_provider):
        self.admin_provider = admin_provider

    def execute(self, admin):
        if type(admin) is not Admin:
            raise ValueError("Admin must be passed")
        if admin.id is None or admin.username is None or admin.password is None:
            raise ValueError("Some fields are missing")
        if admin.id in [ad.id for ad in self.admin_provider.get_admins()]:
            raise ValueError("id already used")
        self.admin_provider.add_admin(admin)