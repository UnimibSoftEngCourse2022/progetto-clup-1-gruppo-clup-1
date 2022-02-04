from src.clup.entities.admin import Admin
import uuid


class AdminRegisterUsecase:
    def __init__(self, admin_provider):
        self.admin_provider = admin_provider

    def execute(self, username, password):
        admin_id = uuid.uuid1()
        if not username or not password:
            raise ValueError('missing fields')
        if username in [adm.username for adm in self.admin_provider.get_admins()]:
            raise ValueError('username already present')
        admin = Admin(admin_id, username, password)
        self.admin_provider.add_admin(admin)
