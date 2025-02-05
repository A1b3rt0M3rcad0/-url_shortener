from datetime import datetime, timezone
from sqlalchemy import String, Integer, Column, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base


class User(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    url = relationship('Url', back_populates='users', cascade='all, delete-orphan')

class Url(Base):

    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    link = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship(User, back_populates='urls')
