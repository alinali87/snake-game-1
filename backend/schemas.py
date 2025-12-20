from datetime import datetime

from pydantic import BaseModel


class ScoreBase(BaseModel):
    player_name: str
    score: int


class ScoreCreate(ScoreBase):
    pass


class Score(ScoreBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
