class LoadUser:
    def __init__(self, user_provider):
        self.user_provider = user_provider

    def execute(self, user_id):
        user = None
        for u in self.user_provider.get_users():
            if u.id == user_id:
                user = u

        if user is None:
            raise ValueError('unexistent user id')

        return user
