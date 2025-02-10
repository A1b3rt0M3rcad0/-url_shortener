from sqlalchemy import Column, String, Integer, ForeignKey
from src.infra.db.settings.base import Base

class Urls(Base):

    __tablename__ = 'urls'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    link = Column(String, nullable=False)
    shortened_link  = Column(String, nullable=False)
