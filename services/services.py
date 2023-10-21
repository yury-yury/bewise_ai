import asyncio
from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import Question, RequestBody
from .external_requests import request_quiz_questions, get_previous_question


async def request_my(data: RequestBody, db: AsyncSession) -> Optional[Question]:
    """
    The asynchronous request_my function contains the main endpoint logic. Takes as arguments the Contents
    of the request body in the form of an object of the RequestBody class and an asynchronous connection
    session with the database. Returns the result obtained from the previous request to
    a third-party API or an empty object if there were no requests.
    """
    result = await get_previous_question()
    if data.questions_num:
        count: int = data.questions_num
        asyncio.create_task(request_quiz_questions(count, db))
    else:
        raise HTTPException(status_code=400, detail='The questions_num parameter must be specified')
    return result
