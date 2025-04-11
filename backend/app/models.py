from sqlalchemy import Column, String, Integer, DateTime, Boolean
from .database import Base


class Switch(Base):
    __tablename__ = "switches"

    id = Column(String, primary_key=True)
    user_email = Column(String)
    name = Column(String)
    content = Column(String)
    interval = Column(Integer)
    expiration_datetime = Column(DateTime)
    is_active = Column(Boolean)
