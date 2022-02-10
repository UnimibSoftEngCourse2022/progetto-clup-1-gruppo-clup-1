from sqlalchemy import Column, Integer, String

from . import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class Reservation(Base):
    id = Column(Integer, primary_key=True)
    aisle_id = Column(Integer)
    user_id = Column(Integer)