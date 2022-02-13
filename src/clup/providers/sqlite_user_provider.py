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
            model_user = models.User(
                uuid=user.id,
                username=user.username,
                password=user.password,
            )
            session.add(model_user)

    def remove_user(self, user_id):
        with Session(self.engine) as session, session.begin():
            session.query(models.User).\
                filter(models.User.uuid == user_id).delete()

    def update_user(self, user):
        with Session(self.engine) as session, session.begin():
            query = session.query(models.User).\
                filter(models.User.uuid == user.id)
            query.update({
                models.User.username: user.username,
                models.User.password: user.password,
            })
