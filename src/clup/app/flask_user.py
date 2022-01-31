from flask_login import UserMixin


class FlaskUser(UserMixin):
    def __init__(self, id):
        self.id = id