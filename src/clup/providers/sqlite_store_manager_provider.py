from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.clup.database import models
from src.clup.entities.store_manager import StoreManager
from src.clup.providers.store_manager_provider_abc \
    import StoreManagerProvider


class SqliteStoreManagerProvider(StoreManagerProvider):
    def __init__(self, engine):
        self.engine = engine

    def get_store_managers(self):
        with Session(self.engine) as session, session.begin():
            model_managers = session.query(models.Account).filter(models.Account.type == 'store_manager').all()
            managers = [StoreManager(mm.uuid, mm.username, mm.password_hash)
                        for mm in model_managers]
            return managers

    def create_new_store_manager(self, storemanager_id, secret):
        with Session(self.engine) as session, session.begin():
            model_storemanager_sk = models.StoreManagerSecretKey(
                store_manager_uuid=storemanager_id,
                secret_key=secret,
                active=False
            )
            session.add(model_storemanager_sk)

    def get_id_from_secret(self, secret):
        with Session(self.engine) as session, session.begin():
            managers = session.query(models.StoreManagerSecretKey) \
                .filter(models.StoreManagerSecretKey.secret_key == secret,
                        models.StoreManagerSecretKey.active == 0).all()
            if len(managers) != 1:
                raise ValueError("wrong secret key")

            return managers[0].store_manager_uuid

    def add_manager(self, store_manager):
        try:
            with Session(self.engine) as session, session.begin():
                manager_model = models.Account(
                    uuid=store_manager.id,
                    username=store_manager.username,
                    password_hash=store_manager.password_hash,
                    type='store_manager'
                )
                session.add(manager_model)
                session.query(models.StoreManagerSecretKey) \
                    .filter(models.StoreManagerSecretKey.store_manager_uuid == store_manager.id) \
                    .update({models.StoreManagerSecretKey.active: True})
        except IntegrityError:
            raise ValueError('username or id already used')

    def delete_store_manager(self, manager_id):
        if manager_id not in [m.id for m in self.get_store_managers()]:
            raise ValueError('Unexistent manager id')

        with Session(self.engine) as session, session.begin():
            session.query(models.Account) \
                .filter(models.Account.uuid == manager_id,
                        models.Account.type == 'store_manager').delete()
            session.query(models.StoreManagerSecretKey) \
                .filter(models.StoreManagerSecretKey.store_manager_uuid == manager_id) \
                .delete()

    def update(self, store_manager):
        if store_manager.id not in [m.id for m in self.get_store_managers()]:
            raise ValueError('Unexistent manager id')

        with Session(self.engine) as session, session.begin():
            query = session.query(models.Account) \
                .filter(models.Account.uuid == store_manager.id,
                        models.Account.type == 'store_manager')
            query.update({
                models.Account.username: store_manager.username,
                models.Account.password_hash: store_manager.password_hash,
            })

    def get_manager(self, manager_id):
        with Session(self.engine) as session, session.begin():
            manager_model = session.query(models.Account) \
                .filter(models.Account.uuid == manager_id,
                        models.Account.type == 'store_manager') \
                .all()
            if len(manager_model) != 1:
                raise ValueError('could not find any manager')
            manager_model = manager_model[0]
            manager = StoreManager(id=manager_model.uuid,
                                   username=manager_model.username,
                                   password_hash=manager_model.password_hash)
            return manager
