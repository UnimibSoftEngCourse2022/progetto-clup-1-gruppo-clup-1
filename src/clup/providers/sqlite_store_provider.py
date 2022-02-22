from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.store import Store
from src.clup.entities.store_manager import StoreManager
from src.clup.providers.store_provider_abc import StoreProvider


class SqliteStoreProvider(StoreProvider):
    def __init__(self, engine):
        self.engine = engine

    def get_stores(self):
        with Session(self.engine) as session, session.begin():
            model_stores = session.query(models.Store).all()
            stores = [Store(ms.uuid, ms.name, ms.address, ms.secret)
                      for ms in model_stores]
            return stores

    def add_store(self, store):
        with Session(self.engine) as session, session.begin():
            if store.id in [s.id for s in self.get_stores()]:
                raise ValueError("store_id already present")

            model_store = models.Store(
                uuid=store.id,
                name=store.name,
                address=store.address,
                secret=store.secret,
            )
            session.add(model_store)

    def update_store(self, store):
        if store.id not in [s.id for s in self.get_stores()]:
            raise ValueError("store_id not present, unable to update")

        with Session(self.engine) as session, session.begin():
            query = session.query(models.Store). \
                filter(models.Store.uuid == store.id)
            query.update({
                models.Store.name: store.name,
                models.Store.address: store.address,
                models.Store.secret: store.secret,
            })

    def delete_store(self, store_id):
        if store_id not in [s.id for s in self.get_stores()]:
            raise ValueError("store_id not present, unable to update")

        with Session(self.engine) as session, session.begin():
            session.query(models.Store). \
                filter(models.Store.uuid == store_id).delete()
            query = session.query(models.StoreAisle). \
                filter(models.StoreAisle.store_uuid == store_id)
            store_aisle_ids = [msa.aisle_uuid for msa in query.all()]
            query.delete()
            session.query(models.Aisle). \
                filter(models.Aisle.uuid.in_(store_aisle_ids)).delete()

    def get_admin_ids(self, store_id):
        with Session(self.engine) as session, session.begin():
            model_store_admins = session.query(models.StoreAdmin). \
                filter(models.StoreAdmin.store_uuid == store_id).all()
            return [msa.admin_uuid for msa in model_store_admins]

    def add_manager_to_store(self, store_id, manager_id):
        with Session(self.engine) as session, session.begin():
            new_ssm = models.StoreStoreManager(
                store_manager_uuid=manager_id,
                store_uuid=store_id
            )
            session.add(new_ssm)

    def get_store_manager_by_username(self, username):
        with Session(self.engine) as session, session.begin():
            sm = session.query(models.StoreManager) \
                .filter(models.StoreManager.username == username).all()
            if len(sm) == 0:
                raise ValueError("unable to find store manager")

            store_manager_model = sm[0]
            store_manager = StoreManager(
                id=store_manager_model.uuid,
                username=store_manager_model.username,
                password=store_manager_model.password
            )

            return store_manager

    def get_store_from_manager_id(self, manager_id):
        with Session(self.engine) as session, session.begin():
            store_id = session.query(models.StoreStoreManager.store_uuid) \
                .filter(models.StoreStoreManager.store_manager_uuid == manager_id).all()
            if len(store_id) != 1:
                raise ValueError("unable to find store connected to this manager")

            store_id = store_id[0][0]

            stores = self.get_stores()

            store = [store for store in stores if store.id == store_id]

            if len(store) != 1:
                raise ValueError("unable to find store with this id")

            return store[0]

    def update_secret_key(self, manager_id, secret_key):
        with Session(self.engine) as session, session.begin():
            session.query(models.StoreManagerSecretKey) \
                .filter(models.StoreManagerSecretKey.store_manager_uuid == manager_id) \
                .update({models.StoreManagerSecretKey.secret_key: secret_key})

    def get_store_id_from_name_and_address(self, store_name, store_address):
        with Session(self.engine) as session, session.begin():
            store = session.query(models.Store)\
                        .filter(models.Store.name == store_name,
                                models.Store.address == store_address).all()

            if len(store) != 1:
                raise ValueError("unable to find a store")

            return store[0].uuid
