from sqlalchemy.orm import Session

import src.clup.database.models as models
from src.clup.entities.store import Store
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
