class UserLoginUseCase:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, user_id, password):
        if user_id not in [user.id for user in self.user_provider.get_users()]:
            raise ValueError("user_id non valido")
        for user in self.user_provider.get_users():
            if user.id == user_id:
                if user.password != password:
                    raise ValueError("password non valida")
                else:
                    return True
        return False