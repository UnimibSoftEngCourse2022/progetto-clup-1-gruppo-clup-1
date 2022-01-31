class BasicUserProvider:
    def __init__(self):
        self.users = {}

    def get_users(self):
        return self.users.values()

    def add_user(self, user):
        self.users[user.id] = user

    def remove_user(self, user_id):
        if user_id not in self.users.keys():
            raise ValueError("user-id not existing")
        del self.users[user_id]