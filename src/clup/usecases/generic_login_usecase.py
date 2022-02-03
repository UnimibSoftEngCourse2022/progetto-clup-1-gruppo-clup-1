from src.clup.usecases.admin_login_usecase import AdminLoginUseCase
from src.clup.usecases.user_login_usecase import UserLoginUseCase


class GenericLoginUsecase:
    def __init__(self, admin_provider, user_provider):
        self.admin_provider = admin_provider
        self.user_provider = user_provider

    def execute(self, username, password):
        try:
            user_id = UserLoginUseCase.execute(self, username, password)
            return user_id, "user"
        except ValueError:
            try:
                admin_id = AdminLoginUseCase.execute(self, username, password)
                return admin_id, "admin"
            except ValueError:
                raise ValueError("wrong credentials")
