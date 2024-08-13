from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from settings import Base


class TodoModel(Base):
    __tablename__ = 'todo'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    created_date = Column(DateTime, default=datetime.utcnow)