from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    username = Column(String)
    password = Column(String)


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    uuid = Column(String)
    aisle_id = Column(String, ForeignKey('aisle.uuid'))
    user_id = Column(String, ForeignKey('user.uuid'))


class Aisle(Base):
    __tablename__ = 'aisle'
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    name = Column(String)
    categories = Column(String)
    capacity = Column(Integer)


class Store(Base):
    __tablename__ = 'store'
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    name = Column(String)
    address = Column(String)
    secret = Column(String)  # TODO unique=True


class StoreAisle(Base):
    __tablename__ = 'store_aisle'
    id = Column(Integer, primary_key=True)
    store_uuid = Column(String, ForeignKey('store.uuid'))
    aisle_uuid = Column(String, ForeignKey('aisle.uuid'), unique=True)


class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    username = Column(String)
    password = Column(String)


class StoreAdmin(Base):
    __tablename__ = 'store_admin'
    id = Column(Integer, primary_key=True)
    admin_uuid = Column(String, ForeignKey('admin.id'), unique=True)
    store_uuid = Column(String, ForeignKey('store.id'))


class Appointment(Base):
    __tablename__ = 'appointment'
    id = Column(Integer, primary_key=True)
    reservation_uuid = Column(String, ForeignKey('reservation.uuid'))
    store_id = Column(String, ForeignKey('store.uuid'))
    date_time = Column(DateTime)


class StoreManager(Base):
    __tablename__ = 'store_manager'
    id = Column(Integer, primary_key=True)
    uuid = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)


class StoreManagerSecretKey(Base):
    __tablename__ = 'store_manager_secretkey'
    id = Column(Integer, primary_key=True)
    store_manager_uuid = Column(String, ForeignKey('store_manager.uuid'))
    secret_key = Column(String)
    active = Column(Boolean)


def create_initial_data(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    u1 = User(uuid=1, username='tizio', password='caio')
    u2 = User(uuid=2, username='mario', password='rossi')

    r1 = Reservation(uuid=1000, aisle_id=10, user_id=1)
    r2 = Reservation(uuid=2000, aisle_id=20, user_id=2)

    a1 = Aisle(uuid=10, name='aisle1', categories='1,2', capacity=10)
    a2 = Aisle(uuid=20, name='aisle2', categories='3,4', capacity=5)

    s1 = Store(uuid=100, name='Esselunga', address='Milano', secret='0')

    s1_a1 = StoreAisle(store_uuid=100, aisle_uuid=10)
    s1_a2 = StoreAisle(store_uuid=100, aisle_uuid=20)

    with Session(engine) as session, session.begin():
        session.add(u1)
        session.add(u2)
        session.add(r1)
        session.add(r2)
        session.add(a1)
        session.add(a2)
        session.add(s1)
        session.add(s1_a1)
        session.add(s1_a2)
