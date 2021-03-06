from sqlalchemy import Column, Integer, String
from . import Base


class User(Base):
    __tablename__ = 'user'
    from_id = Column(Integer, primary_key=True, unique=True)
    class_ = Column(String(3), nullable=False)
    group = Column(Integer, nullable=False)