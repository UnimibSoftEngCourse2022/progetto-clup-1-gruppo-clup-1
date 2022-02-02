class AdminLoginUseCase:
    def __init__(self, admin_provider):
        self.admin_provider = admin_provider

    def execute(self, admin_username, password):
        if admin_username not in [ad.username for ad in self.admin_provider.get_admins()]:
            raise ValueError("wrong id")
        for admin in self.admin_provider.get_admins():
            if admin.username == admin_username:
                if admin.password != password:
                    raise ValueError("Wrong password")
                else:
                    return admin.id
        return False