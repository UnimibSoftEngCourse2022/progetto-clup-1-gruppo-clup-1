from src.clup.entities.store_manager import StoreManager
from sqlalchemy.orm import Session

from src.clup.database import models


class SqliteStoreManagerProvider:
    def __init__(self, engine):
        self.engine = engine

    def create_new_store_manager(self, store_manager_id, secret_key):
        with Session(self.engine) as session, session.begin():
            model_store_manager_sk = models.StoreManagerSecretKey(
                store_manager_uuid=store_manager_id,
                secret_key=secret_key,
                active=False
            )
            session.add(model_store_manager_sk)

    def get_manager_id_from_sk(self, secret_key):
        with Session(self.engine) as session, session.begin():
            managers = session.query(models.StoreManagerSecretKey) \
                .filter(models.StoreManagerSecretKey.secret_key == secret_key,
                        models.StoreManagerSecretKey.active == 0).all()
            print(managers)
            if len(managers) != 1:
                raise ValueError("wrong secret key")

            return managers[0].store_manager_uuid

    def add_manager(self, id, username, password):
        with Session(self.engine) as session, session.begin():
            manager_model = models.StoreManager(
                uuid=id,
                username=username,
                password=password
            )
            session.add(manager_model)
            session.query(models.StoreManagerSecretKey) \
                .filter(models.StoreManagerSecretKey.store_manager_uuid == id) \
                .update({models.StoreManagerSecretKey.active: True})

    def delete_store_manager(self, manager_id):
        with Session(self.engine) as session, session.begin():
            session.query(models.StoreManager) \
                .filter(models.StoreManager.uuid == manager_id) \
                .delete()
            session.query(models.StoreManagerSecretKey) \
                .filter(models.StoreManagerSecretKey.store_manager_uuid == manager_id) \
                .delete()

    def get_manager(self, manager_id):
        with Session(self.engine) as session, session.begin():
            manager_model = session.query(models.StoreManager) \
                .filter(models.StoreManager.uuid == manager_id) \
                .all()
            if len(manager_model) != 1:
                raise ValueError('could not find any manager')
            manager_model = manager_model[0]
            manager = StoreManager(id=manager_model.uuid,
                                   username=manager_model.username,
                                   password=manager_model.password)
            return manager
