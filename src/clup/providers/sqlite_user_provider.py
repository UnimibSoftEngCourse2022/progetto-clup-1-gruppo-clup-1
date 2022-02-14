from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.user import User


class SqliteUserProvider:
    def __init__(self, engine):
        self.engine = engine

    def get_users(self):
        with Session(self.engine) as session, session.begin():
            model_users = session.query(models.User).all()
            users = [User(mu.uuid, mu.username, mu.password)
                     for mu in model_users]
            return users

    def add_user(self, user):
        with Session(self.engine) as session, session.begin():
            if user.id in [u.id for u in self.get_users()]:
                raise ValueError("user_id already present")
            model_user = models.User(
                uuid=user.id,
                username=user.username,
                password=user.password,
            )
            session.add(model_user)

    def remove_user(self, user_id):
        with Session(self.engine) as session, session.begin():
            if user_id not in [u.id for u in self.get_users()]:
                raise ValueError("user_id not present")
            session.query(models.User). \
                filter(models.User.uuid == user_id).delete()

    def update_user(self, user):
        with Session(self.engine) as session, session.begin():
            if user.id not in [u.id for u in self.get_users()]:
                raise ValueError("user_id already present")

            query = session.query(models.User). \
                filter(models.User.uuid == user.id)
            query.update({
                models.User.username: user.username,
                models.User.password: user.password,
            })

