class LoadAdminUseCase:
    def __init__(self, admin_provider):
        self.admin_provider = admin_provider

    def execute(self, admin_id):
        admin = None
        for a in self.admin_provider.get_admins():
            if a.id == admin_id:
                admin = a

        if admin is None:
            raise ValueError('unexistent admin id')

        return admin
