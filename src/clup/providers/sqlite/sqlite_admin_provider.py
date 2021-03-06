from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.admin import Admin
from src.clup.providers.abc.admin_provider import AdminProvider


class SqliteAdminProvider(AdminProvider):
    def __init__(self, engine):
        self.engine = engine

    def get_admins(self):
        with Session(self.engine) as session, session.begin():
            model_admins = session.query(models.Account).filter(models.Account.type == 'admin').all()
            admins = [Admin(ma.uuid, ma.username, ma.password_hash)
                      for ma in model_admins]
            return admins

    def get_admin(self, admin_id):
        with Session(self.engine) as session, session.begin():
            ma = session.query(models.Account) \
                .filter(models.Account.type == 'admin',
                        models.Account.uuid == admin_id).first()
            if not ma:
                raise ValueError('unexistent admin id')
            admin = Admin(ma.uuid, ma.username, ma.password_hash)
            return admin

    def add_admin(self, admin):
        if admin.username in [a.username for a in self.get_admins()]:
            raise ValueError('admin username already used')

        try:
            with Session(self.engine) as session, session.begin():
                model_admin = models.Account(
                    uuid=admin.id,
                    username=admin.username,
                    password_hash=admin.password_hash,
                    type='admin'
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
            raise ValueError('account id already used')

    def remove_admin(self, admin_id):
        if admin_id not in [a.id for a in self.get_admins()]:
            raise ValueError("unexistent admin id")

        with Session(self.engine) as session, session.begin():
            session.query(models.Account). \
                filter(models.Account.uuid == admin_id,
                       models.Account.type == 'admin').delete()
            session.query(models.StoreAdmin). \
                filter(models.StoreAdmin.admin_uuid == admin_id).delete()

    def update(self, admin):
        if admin.id not in [a.id for a in self.get_admins()]:
            raise ValueError("unexistent admin id")

        with Session(self.engine) as session, session.begin():
            query = session.query(models.Account). \
                filter(models.Account.uuid == admin.id)
            query.update({
                models.Account.username: admin.username,
                models.Account.password_hash: admin.password_hash,
            })

    def get_store_id(self, admin_id):
        if admin_id not in [a.id for a in self.get_admins()]:
            raise ValueError("unexistent admin id")

        with Session(self.engine) as session, session.begin():
            model_store_admin = session.query(models.StoreAdmin). \
                filter(models.StoreAdmin.admin_uuid == admin_id).first()
            return model_store_admin.store_uuid
