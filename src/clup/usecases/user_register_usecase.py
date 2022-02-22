import uuid

from werkzeug.security import generate_password_hash

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

        pw_hash = generate_password_hash(password)
        user = User(user_id, username, pw_hash)
        self.user_provider.add_user(user)

        return user_id
