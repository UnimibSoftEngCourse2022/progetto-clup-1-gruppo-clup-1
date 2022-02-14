class UserChangePasswordUseCase:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, username, old_password, new_password):
        if username not in [user.username for user in self.user_provider.get_users()]:
            raise ValueError("user_id non valido")
        if not new_password:
            raise ValueError("nuova password non valida")
        for user in self.user_provider.get_users():
            if user.username == username:
                if user.password != old_password:
                    raise ValueError("password non valida")
                else:
                    user = self.user_provider.get_user(user.id)
                    user.password = new_password
                    self.user_provider.update_user(user)
