from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.infra.db.settings.base import Base
from src.infra.db.entities.url import Urls

class Users(Base):

    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)

    urls = relationship(Urls, backref="user", lazy="subquery")