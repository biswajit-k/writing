import threading
import time
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

engine = create_engine('postgresql://postgres:root@localhost:5432/sample', isolation_level="READ COMMITTED")

Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)


s2 = session_factory()

with session_factory() as s:
    a_s1 = User(name="alice")
    s.add(a_s1)
    s.commit()

def f1():
    s1 = session_factory()
    a_s1 = s1.query(User).filter_by(name="alice").one()
    print("f1: got the object, now sleeping for 3s....")
    time.sleep(3)
    s1.expire(a_s1)
    print(f"f1: expired object, now getting again: {a_s1.name}")

def f2():
    s2 = session_factory()
    print("f2: fetching the object")
    a_s2 = s2.query(User).filter_by(name="alice").one()
    print("f2: got the object in f2")
    a_s2.name = "new name"
    s2.commit()
    print(f"f2: comitted the updates")

threading.Thread(target=f1).start()
time.sleep(0.3)
threading.Thread(target=f2).start()

# session = Session()

# # Add duplicate records
# session.add_all([
#     User(name='Alice'),
#     User(name='Alice')  # Duplicate entry
# ])
# session.commit()

# # Query for 'Alice'
# alice1 = session.query(User).filter_by(name='Alice').all()
# print(alice1)
# alice2 = session.query(User).filter_by(name='Alice').first()

# print(alice1 is alice2)  # True, the same object is returned
