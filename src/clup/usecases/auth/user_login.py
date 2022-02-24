class UserLogin:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, username, password):
        if username not in [user.username for user in self.user_provider.get_users()]:
            raise ValueError("user_id non valido")
        for user in self.user_provider.get_users():
            if user.username == username:
                if user.password != password:
                    raise ValueError("password non valida")
                else:
                    return user.id
        return False
