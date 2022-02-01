class UserChangePasswordUseCase:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, user_id, old_password, new_password):
        if user_id not in [user.id for user in self.user_provider.get_users()]:
            raise ValueError("user_id non valido")
        if not new_password:
            raise ValueError("nuova password non valida")
        for user in self.user_provider.get_users():
            if user.id == user_id:
                if user.password != old_password:
                    raise ValueError("password non valida")
                else:
                    self.user_provider.get_user(user_id).password = new_password
