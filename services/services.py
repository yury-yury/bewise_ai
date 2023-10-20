from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import Question
from db import models
from .external_requests import request_quiz_questions, PREVIOUS_QUESTION, get_pervious_question


async def request_my(data: dict, db: AsyncSession) -> Optional[Question]:
    if data.get('questions_num', None):
        count: int = data['questions_num']
        await request_quiz_questions(count, db)
    else:
        raise HTTPException(status_code=400, detail='Параметр questions_num должен быть указан')
    return get_pervious_question()


