import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db_classes import Base, User, Reservation, Aisle, Store, StoreAisle, Admin, StoreAdmin

path = os.path.dirname(os.path.abspath(__file__)) + "/clup.sqlite"
engine = create_engine(f'sqlite:///{path}')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)


def db_populate():
    add_session = Session(engine)
    query = add_session.query(User.uuid, User.username, User.password)
    users = query.all()

    if len(users) == 0:
        user1 = User(uuid=1, username='tizio', password='caio')
        user2 = User(uuid=2, username='mario', password='rossi')
        add_session.add(user1)
        add_session.add(user2)
        add_session.commit()

    query = add_session.query(Reservation.id)
    reservations = query.all()

    if len(reservations) == 0:
        reservation1 = Reservation(uuid=1000, aisle_id=10, user_id=1)
        reservation2 = Reservation(uuid=2000, aisle_id=20, user_id=2)
        add_session.add(reservation1)
        add_session.add(reservation2)
        add_session.commit()

    query = add_session.query(Aisle.id)
    aisles = query.all()

    if len(aisles) == 0:
        aisle1 = Aisle(uuid=10, name='aisle1', categories='1,2', capacity=10)
        aisle2 = Aisle(uuid=20, name='aisle2', categories='3,4', capacity=5)
        add_session.add(aisle1)
        add_session.add(aisle2)
        add_session.commit()

    query = add_session.query(Store.id)
    stores = query.all()

    if len(stores) == 0:
        store1 = Store(uuid=100, name='Esselunga', address='Milano', secret_key=0)
        add_session.add(store1)
        add_session.commit()

    query = add_session.query(StoreAisle.id)
    store_aisles = query.all()

    if len(store_aisles) == 0:
        store_aisles1 = StoreAisle(store_uuid=100, aisle_uuid=10)
        store_aisles2 = StoreAisle(store_uuid=100, aisle_uuid=20)
        add_session.add(store_aisles1)
        add_session.add(store_aisles2)
        add_session.commit()


db_populate()
