from src.clup.usecases.admin_login_usecase import AdminLoginUseCase
from src.clup.usecases.user_login_usecase import UserLoginUseCase


class GenericLoginUsecase:
    def __init__(self, admin_provider, user_provider, store_manager_provider):
        self.admin_provider = admin_provider
        self.user_provider = user_provider
        self.store_manager_provider = store_manager_provider

    def execute(self, username, password):
        if username in [u.username for u in self.user_provider.get_users()]:
            for user in self.user_provider.get_users():
                if user.username == username:
                    if user.password == password:
                        return user.id, 'user'
                    else:
                        raise ValueError("wrong password")

            raise ValueError("problem while searching for a user")

        elif username in [a.username for a in self.admin_provider.get_admins()]:
            for admin in self.admin_provider.get_admins():
                if admin.username == username:
                    if admin.password == password:
                        return admin.id, 'admin'
                    else:
                        raise ValueError("wrong password")

            raise ValueError("problem while searching for an admin")

        elif username in [m.username for m in self.store_manager_provider.get_store_managers()]:
            for manager in self.store_manager_provider.get_store_managers():
                if manager.username == username:
                    if manager.password == password:
                        return manager.id, 'store_manager'
                    else:
                        raise ValueError("wrong password")

            raise ValueError("problem while searching for a store manager")

        else:
            raise ValueError("wrong credentials")
