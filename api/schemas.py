import datetime
from pydantic import BaseModel


class Question(BaseModel):
    """
    The Question class is a data schema to be presented at the endpoint in the form of JSON.
    Inherited from the parent class BaseModel from the pydentic library.
    """
    id: int
    question: str
    answer: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class RequestBody(BaseModel):
    questions_num: int
