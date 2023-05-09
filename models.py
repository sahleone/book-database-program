# Models for the application
# Author: Rhys
# Created: 09 May 2021

# Imports
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    Date
)

from sqlalchemy.orm import declarative_base, sessionmaker

# Create DataBase
## Create engine
engine = create_engine('sqlite:///books.db', echo=True)

## Create a session
Session = sessionmaker(bind=engine)
session = Session()

## Initialize Base
Base = declarative_base()

# Create a model
class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column('Title', String)
    author = Column('Author', String)
    published_date = Column('Published', Date)
    price = Column('Price', Float)

    def __repr__(self):
        return f"Book(title={self.title}, author={self.author}, published={self.published_date}, price={self.price})"
