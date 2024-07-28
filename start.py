from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine("sqlite://", echo=True)

# define the database base class to be inherited by User
class Base(DeclarativeBase):
	pass

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String, nullable=False)


# create the tables
Base.metadata.create_all(engine)

session_factory = sessionmaker(bind=engine)
session = session_factory()


john = User(fullname="John Doe")
session.add(john)
session.commit()
session.expire(john)
print(john.fullname)


