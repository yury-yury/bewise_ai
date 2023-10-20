from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import Question
import services
from db.sessions import get_db
from services.services import request_my

question_router = APIRouter()


@question_router.post('/', response_model=Optional[Question])
async def request_quiz_questions(data: dict, db: AsyncSession = Depends(get_db)) -> Optional[Question]:
    return await request_my(data, db)
