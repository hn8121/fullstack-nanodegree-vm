#! /usr/bin/env python3
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from passlib.apps import custom_app_context as pwd_context
import random
import string
from itsdangerous import(
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

Base = declarative_base()
secret_key = ''.join(random.choice(
    string.ascii_uppercase + string.digits) for x in range(32))
#    string.ascii_uppercase + string.digits) for x in xrange(32))


Base = declarative_base()


class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), index=true, nullable=False)
    email = Column(String(80), nullable=False)
    picture = Column(String(250))
    password_hash = Column(String(64))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'picture': self.picture
        }

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            print("expired")
            return None
        except BadSignature:
            # Invalid Token
            print("invalid token")
            return None
        user_id = data['id']
        return user_id


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    city = Column(String(100))
    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship(Owner)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'owner_id': self.owner_id
        }


class Player(Base):
    __tablename__ = 'player'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    uniform_num = Column(String(3))
    position = Column(String(100))
    salary = Column(String(20))
    team_id = Column(Integer, ForeignKey('team.id'))
    team = relationship(Team)
    owner_id = Column(Integer, ForeignKey('owner.id'))
    owner = relationship(Owner)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'uniform_num': self.uniform_num,
            'position': self.position,
            'salary': self.salary
        }


engine = create_engine('sqlite:///catalog.db')

Base.metadata.create_all(engine)
