class BasicUserProvider:
    def __init__(self):
        self.users = {}

    def get_users(self):
        return self.users.values()

    def add_users(self, user):
        self.users[user.id] = user

    # TODO remove_user