from datetime import datetime
from typing import Optional
import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import models
from api.schemas import Question


PREVIOUS_QUESTION: Optional[Question] = None


async def get_previous_question() -> Optional[Question]:
    """
    The asynchronous get_previous_question function, when called, obtains the value
    of the PREVIOUS_QUESTION variable from the global scope and returns it.
    """
    return PREVIOUS_QUESTION


async def save_question(instance: models.Question, db: AsyncSession) -> None:
    """
    The asynchronous save_question function takes as arguments a data model instance
    and an asynchronous database connection session. When called, it saves an instance in the database,
    forms an instance of the data schema based on this instance, and writes to the value of a global variable.
    """
    global PREVIOUS_QUESTION

    PREVIOUS_QUESTION = Question(
        id=instance.id,
        question=instance.question,
        answer=instance.answer,
        created_at=instance.created_at
    )
    async with db as db:
        db.add(instance)
        await db.commit()


async def check_question(qid: int, db: AsyncSession) -> bool:
    """
    The asynchronous check_question function takes as arguments the value of the id field as an integer
    and the asynchronous session of the connection to the database. When called, it checks the existence
    of a data instance in the database with the given argument. If present, returns False otherwise True.
    """
    try:
        await db.execute(select(Question).filter(Question.id == qid))
    except Exception:
        return True
    else:
        return False


async def get_question(session: aiohttp.ClientSession) -> dict:
    """
    The asynchronous get_question function takes a request session to an external API as an argument.
    When called, it makes a request and returns the received data in the form of a dictionary.
    """
    url = 'https://jservice.io/api/random?count=1'
    async with session.get(url=url) as response:
        question_json = await response.json()
        return question_json[0] if question_json else None


async def request_quiz_questions(count: int, db: AsyncSession) -> None:
    """
    The asynchronous function request_quiz_questions takes as arguments the number of successful requests
    to a third-party API as an integer and the asynchronous session of connecting to the database.
    Contains the necessary logic for executing requests. Organizes joint asynchronous work of service functions.
    """
    while count > 0:
        async with aiohttp.ClientSession() as session:
            question = await get_question(session)
            if await check_question(question['id'], db):
                unic_question = models.Question(
                    id=question['id'],
                    question=question['question'],
                    answer=question['answer'],
                    created_at=datetime.strptime(question['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                )
                await save_question(unic_question, db)
                count -= 1
