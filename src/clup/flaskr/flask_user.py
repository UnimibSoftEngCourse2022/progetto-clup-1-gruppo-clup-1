from flask_login import UserMixin


class FlaskUser(UserMixin):
    def __init__(self, u_id, type):
        self.id = u_id
        self.type = type

    def get_id(self):
        return self.id

    def get_type(self):
        return self.type
