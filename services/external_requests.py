from datetime import datetime
from time import strptime
from typing import Optional
import aiohttp
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import models
import services
from db.sessions import get_db
from api.schemas import Question


PREVIOUS_QUESTION: Optional[Question] = None

def get_pervious_question() -> Optional[Question]:
    return PREVIOUS_QUESTION

async def save_question(instance: models.Question, db: AsyncSession):
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

    print('PREVIOUS_QUESTION=', PREVIOUS_QUESTION)


async def check_question(qid: int, db: AsyncSession) -> bool:
    try:
        await db.execute(select(Question).filter(Question.id == qid))
    except Exception:
        return True
    else:
        return False


async def get_question(session):
    url = 'https://jservice.io/api/random?count=1'
    async with session.get(url=url) as response:
        question_json = await response.json()
        return question_json[0] if question_json else None


async def request_quiz_questions(count: int, db: AsyncSession):
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
