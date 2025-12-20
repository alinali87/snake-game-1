from datetime import datetime

from database import Base
from sqlalchemy import Column, DateTime, Integer, String


class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, index=True)
    score = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
