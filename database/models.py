from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):

    __tablename__ ='users'
    __tableargs__ = {
        'comment' : 'Информация о пользователях'
    }

    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    name_id = Column(
        String(128),
        nullable=False
    )

    password = Column(
        String(128),
        nullable=False
    )

    def __repr__(self):
        return f'{self.id} {self.name_id} {self.password}'
    
class Data(Base):

    __tablename__ = 'data'
    __tableargs__ = {
        'comment' : 'Данные, внесенные пользователями'
    }
    
    id = Column(
        Integer,
        nullable=False,
        unique=True,
        primary_key=True,
        autoincrement=True
    )
    text = Column(
        Text,
        comment='Данные пользователя'
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id', ondelete='CASCADE')
    )

    def __repr__(self):
        return f'{self.id} {self.text}'
    