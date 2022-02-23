from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.user import User
from src.clup.providers.user_provider_abc import UserProvider


class SqliteUserProvider(UserProvider):
    def __init__(self, engine):
        self.engine = engine

    def get_user(self, user_id):
        for user in self.get_users():
            if user.id == user_id:
                return user
        raise ValueError("unable to find user with this id")

    def get_users(self):
        with Session(self.engine) as session, session.begin():
            model_users = session.query(models.Account).filter(models.Account.type == 'user').all()
            users = [User(mu.uuid, mu.username, mu.password_hash)
                     for mu in model_users]
            return users

    def add_user(self, user):
        if user.username in [a.username for a in self.get_users()]:
            raise ValueError('username already used')

        try:
            with Session(self.engine) as session, session.begin():
                model_admin = models.Account(
                    uuid=user.id,
                    username=user.username,
                    password_hash=user.password_hash,
                    type='user'
                )
                session.add(model_admin)
        except IntegrityError:
            raise ValueError('admin id already used')

    def remove_user(self, user_id):
        with Session(self.engine) as session, session.begin():
            if user_id not in [u.id for u in self.get_users()]:
                raise ValueError("user_id not present")
            session.query(models.Account). \
                filter(models.Account.uuid == user_id,
                       models.Account.type == 'user').delete()

    def update(self, user):
        with Session(self.engine) as session, session.begin():
            if user.id not in [u.id for u in self.get_users()]:
                raise ValueError("user_id already present")

            query = session.query(models.Account). \
                filter(models.Account.uuid == user.id,
                       models.Account.type == 'user')
            query.update({
                models.Account.username: user.username,
                models.Account.password_hash: user.password_hash,
            })
