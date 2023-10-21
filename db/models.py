from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Question(Base):
    """
    The Question class is a data model for interacting with the database. Inherited from the base class Base.
    Contains the names and valid data types contained in the columns of the database table.
    """
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime)