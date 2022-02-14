from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.admin import Admin


class SqliteAdminProvider:
    def __init__(self, engine):
        self.engine = engine

    def get_admins(self):
        with Session(self.engine) as session, session.begin():
            model_admins = session.query(models.Admin).all()
            admins = [Admin(ma.uuid, ma.username, ma.password)
                      for ma in model_admins]
            return admins

    def add_admin(self, admin):
        if admin.id in [a.id for a in self.get_admins()]:
            raise ValueError("unable to add new admin, id already used")

        if admin.username in [a.username for a in self.get_admins()]:
            raise ValueError("unable to add new admin, username already used")

        with Session(self.engine) as session, session.begin():
            model_admin = models.Admin(
                uuid=admin.id,
                username=admin.username,
                password=admin.password,
            )
            session.add(model_admin)

    def remove_admin(self, admin_id):
        if admin_id not in [a.id for a in self.get_admins()]:
            raise ValueError("unable to remove admin, id not existing")

        with Session(self.engine) as session, session.begin():
            session.query(models.Admin). \
                filter(models.Admin.uuid == admin_id).delete()

    def update_admin(self, admin):
        if admin.id not in [a.id for a in self.get_admins()]:
            raise ValueError("unable to update admin, id not existing")

        with Session(self.engine) as session, session.begin():
            query = session.query(models.Admin). \
                filter(models.Admin.uuid == admin.id)
            query.update({
                models.Admin.username: admin.username,
                models.Admin.password: admin.password,
            })

    def get_store_id(self, admin_id):
        with Session(self.engine) as session, session.begin():
            model_store_admin = session.query(models.StoreAdmin). \
                filter(models.StoreAdmin.admin_uuid == admin_id).first()
            return model_store_admin.store_uuid
