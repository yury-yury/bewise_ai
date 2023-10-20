import datetime
from pydantic import BaseModel


class Question(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

