from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True)
    aisle_id = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))


engine = create_engine('sqlite:///clup.sqlite')
session = sessionmaker()
session.configure(bind=engine)
Base.metadata.create_all(engine)
