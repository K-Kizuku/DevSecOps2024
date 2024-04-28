import enum
import uuid

from sqlalchemy import Boolean, Column, Enum, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Role(str, enum.Enum):
    admin = 'admin'
    user = 'user'

class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False, default=Role.user)