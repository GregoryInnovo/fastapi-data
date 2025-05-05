from sqlalchemy import Column, String, Integer, DateTime
from app.db.database import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    description = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
