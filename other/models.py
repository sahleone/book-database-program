from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# Create connection to database
## Connection string for sqlite
connectionString = 'sqlite:///users.db'

## Create engine
engine = create_engine(connectionString, echo=True)

## Create base class
Base = declarative_base()

## Create session
Session = sessionmaker(bind=engine)
session =  Session()

# Create tables
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    nickname = Column(String)


    def __repr__(self):
        return f'<User(name={self.name}, fullname={self.fullname},\
              nickname={self.nickname}>'

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    
    users = [
        User(name='Grace', fullname='Grace Hopper', nickname='Pioneer'),
        User(name='Alan', fullname='Alan Turing', nickname='Computer Scientist'),
        User(name='Katherine', fullname='Katherine Johnson', nickname=''),
        User(name='Ada', fullname='Ada Lovelace', nickname='Love'),
        User(name='Tim', fullname='Tim Berners-Lee', nickname='WWW'),
        User(name='Guido', fullname='Guido van Rossum', nickname='Python')
        ]
    session.add_all(users)
    # session.add(users[0])
    # print(session.new)
    # session.new only new records

    session.commit()

    # Update record
    jethro = User(name='Jethr', fullname='Jethro Tull', nickname='Flute')
    session.add(jethro)
    session.commit()

    ## Update record
    jethro.name = 'Jethro'
    session.dirty

    # Rollback
    jethro.nickname = "jetty"
    aang = User(name='Aang', fullname='Avatar Aang', nickname='Aangie')
    session.add(aang)
    print(session.new)
    session.rollback()

    # Delete record
    aang = User(name='Aang', fullname='Avatar Aang', nickname='Aangie')
    ## add aang to db
    session.add(aang)
    session.commit()
    ## delete aang from db
    session.delete(aang)
    session.commit()



query = session.query(User).all()
print(query)

query = session.query(User.name).filter(User.name.like('A%')).all()
print(query)

for user in session.query(User.name).filter(User.name.like('A%')):
    print(user.name)
