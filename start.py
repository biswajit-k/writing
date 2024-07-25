from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, DeclarativeBase, sessionmaker


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

session.autoflush=False		# disable auto flush data

session.begin()		# begin the transaction

john = User(fullname="John Doe")
print(john.fullname)

session.add(john)   # insert row in the user table
session.flush()

session.commit()    # persist the object

session.close()		# end the transaction

