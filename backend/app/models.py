from sqlalchemy import Column, String
from .database import Base


class Repo(Base):
    __tablename__ = "repos"

    username = Column(String)
    id = Column(String, primary_key=True)
    full_name = Column(String)