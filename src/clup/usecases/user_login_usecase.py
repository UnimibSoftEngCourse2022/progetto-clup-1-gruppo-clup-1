class UserLoginUseCase:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, user_id, password):
        for user in self.user_provider.get_users():
            if user.id == user_id and user.password == password:
                return True
        return False