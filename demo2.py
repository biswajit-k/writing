import threading
import random
import time
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

engine = create_engine('postgresql://postgres:root@localhost:5432/sample')

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)

session = session_factory()

user = session.query(User).filter_by(name="babel").one()

print(session.in_transaction())

