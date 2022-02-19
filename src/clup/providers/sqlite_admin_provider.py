from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

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
        if admin.username in [a.username for a in self.get_admins()]:
            raise ValueError('admin username already used')

        try:
            with Session(self.engine) as session, session.begin():
                model_admin = models.Admin(
                    uuid=admin.id,
                    username=admin.username,
                    password=admin.password,
                )
                session.add(model_admin)
        except IntegrityError:
            raise ValueError('admin id already used')

    def add_admin_to_store(self, admin_id, store_id):
        try:
            with Session(self.engine) as session, session.begin():
                model_store_admin = models.StoreAdmin(
                    admin_uuid=admin_id,
                    store_uuid=store_id
                )
                session.add(model_store_admin)
        except IntegrityError:
            raise ValueError('admin id already used')

    def remove_admin(self, admin_id):
        if admin_id not in [a.id for a in self.get_admins()]:
            raise ValueError("unexistent admin id")

        with Session(self.engine) as session, session.begin():
            session.query(models.Admin). \
                filter(models.Admin.uuid == admin_id).delete()
            session.query(models.StoreAdmin). \
                filter(models.StoreAdmin.admin_uuid == admin_id).delete()

    def update_admin(self, admin):
        if admin.id not in [a.id for a in self.get_admins()]:
            raise ValueError("unexistent admin id")

        with Session(self.engine) as session, session.begin():
            query = session.query(models.Admin). \
                filter(models.Admin.uuid == admin.id)
            query.update({
                models.Admin.username: admin.username,
                models.Admin.password: admin.password,
            })

    def get_store_id(self, admin_id):
        if admin_id not in [a.id for a in self.get_admins()]:
            raise ValueError("unexistent admin id")

        with Session(self.engine) as session, session.begin():
            model_store_admin = session.query(models.StoreAdmin). \
                filter(models.StoreAdmin.admin_uuid == admin_id).first()
            return model_store_admin.store_uuid
