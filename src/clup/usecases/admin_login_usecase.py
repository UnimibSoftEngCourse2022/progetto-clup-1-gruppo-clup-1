class AdminLoginUseCase:
    def __init__(self, admin_provider):
        self.admin_provider = admin_provider

    def execute(self, admin_id, password):
        if admin_id not in [ad.id for ad in self.admin_provider.get_admins()]:
            raise ValueError("wrong id")
        for admin in self.admin_provider.get_admins():
            if admin.id == admin_id:
                if admin.password != password:
                    raise ValueError("Wrong password")
                else:
                    return True
        return False