class UserLoginUseCase:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, user_id, password):
        users = self.user_provider.get_users()
        password_valid = False
        if (user_id, password) in users:
            password_valid = True
        return password_valid