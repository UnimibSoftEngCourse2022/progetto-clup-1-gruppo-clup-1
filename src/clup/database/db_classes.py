from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

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
    secret_key = Column(String)  # TODO unique=True


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
