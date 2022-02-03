from flask_login import UserMixin


class FlaskUser(UserMixin):
    def __init__(self, u_id):
        self.id = u_id

    def get_id(self):
        return self.id
