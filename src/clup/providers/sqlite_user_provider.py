from sqlalchemy.orm import Session

from src.clup.database import User, engine
from src.clup.entities import user


class SqliteUserProvider:
    def get_users(self):
        db_session = Session(engine)
        query = db_session.query(User.uuid, User.username, User.password)
        users = query.all()
        user_list = []
        for us in users:
            u = user.User(us[0], us[1], us[2])
            user_list.append(u)
        return user_list

    def add_user(self, user_from_register):
        id = user_from_register.id
        username = user_from_register.username
        password = user_from_register.password
        db_session = Session(engine)
        new_user = User(uuid=id, username=username, password=password)
        db_session.add(new_user)
        db_session.commit()

    def remove_user(self, user_id):
        db_session = Session(engine)
        db_session.query(User).filter(User.uuid == user_id).delete()
        db_session.commit()


up = SqliteUserProvider()
print(up.get_users())
up.add_user(user.User(3, 'lorenzo', 'titta'))
print(up.get_users())
up.remove_user(3)
print(up.get_users())
