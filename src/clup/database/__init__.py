import os

from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

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
    aisle_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.uuid'))


path = os.path.dirname(os.path.abspath(__file__)) + "/clup.sqlite"
engine = create_engine(f'sqlite:///{path}')

session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)

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
    reservation1 = Reservation(aisle_id=10, user_id=1)
    reservation2 = Reservation(aisle_id=20, user_id=2)
    add_session.add(reservation1)
    add_session.add(reservation2)
    add_session.commit()