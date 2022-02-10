import uuid

from src.clup.entities.user import User


class UserRegisterUsecase:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, username, password):
        user_id = str(uuid.uuid1())
        if not username or not password:
            raise ValueError('Null type not valid')
        if username in [usr.username for usr in self.user_provider.get_users()]:
            raise ValueError('username already present')
        user = User(user_id, username, password)
        self.user_provider.add_user(user)
