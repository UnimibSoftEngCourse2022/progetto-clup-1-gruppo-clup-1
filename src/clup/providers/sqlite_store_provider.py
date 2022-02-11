from sqlalchemy.orm import Session

from src.clup.database import Store, engine
from src.clup.entities import store


class SqliteStoreProvider:
    def get_stores(self):
        db_session = Session(engine)
        stores_db = db_session.query(Store).all()
        stores_ent = []
        for st in stores_db:
            store_ent = store.Store(id=st.uuid, name=st.name, address=st.address, secret_key=st.secret_key)
            stores_ent.append(store_ent)
        return stores_ent

    def add_store(self, store_ent):
        db_session = Session(engine)
        new_store = Store(uuid=store_ent.id, name=store_ent.name, address=store_ent.address,
                          secret_key=store_ent.secret_key)
        db_session.add(new_store)
        db_session.commit()

    def remove_store(self, store_id):
        db_session = Session(engine)
        db_session.query(Store).filter(Store.uuid == store_id).delete()
        db_session.commit()

    # TODO def get_queue(self, store_id):

    # TODO def add_to_queue(self, store_id, element):


sp = SqliteStoreProvider()
print(sp.get_stores())
sp.add_store(store.Store(id=200, name='Tigros', address='Sesto', secret_key=0))
print(sp.get_stores())
sp.remove_store(200)
print(sp.get_stores())
