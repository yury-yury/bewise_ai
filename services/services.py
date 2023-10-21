import asyncio
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import Question, RequestBody
from .external_requests import request_quiz_questions, get_previous_question


async def request_my(data: RequestBody, db: AsyncSession) -> Optional[Question]:
    result = await get_previous_question()
    if data.questions_num:
        count: int = data.questions_num
        asyncio.create_task(request_quiz_questions(count, db))
    else:
        raise HTTPException(status_code=400, detail='Параметр questions_num должен быть указан')
    return result
