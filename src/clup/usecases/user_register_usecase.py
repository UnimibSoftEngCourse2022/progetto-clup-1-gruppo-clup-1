from src.clup.entities.user import User


class UserRegisterUsecase:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, user):
        if type(user) is not User:
            raise ValueError("you must be an user")
        if user.id in [usr.id for usr in self.user_provider.get_users()]:
            raise ValueError('user_id already present')
        if not user.id or not user.password:
            raise ValueError('Null type not valid')

        self.user_provider.add_user(user)
