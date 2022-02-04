class LoadUserDataUseCase:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, user_id):
        if user_id not in [user.id for user in self.user_provider.get_users()]:
            raise ValueError("user_id non valido")
        if not user_id:
            raise ValueError("user_id non valido")
        if self.user_provider.get_user(user_id) is None:
            raise ValueError("None!!")
        return self.user_provider.get_user(user_id)
