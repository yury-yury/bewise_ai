from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import Question, RequestBody
from db.sessions import get_db
from services.services import request_my


question_router = APIRouter()


@question_router.post('/', response_model=Optional[Question], )
# @extend_schema(requestbody({"questions_num": int}))
async def request_quiz_questions(data: RequestBody, db: AsyncSession = Depends(get_db)) -> Optional[Question]:
    """
    The request_quiz_questions asynchronous function is an FBV for serving POST requests to the URL '/quest/'.
    Takes data as arguments - the contents of the request body and an asynchronous session of a connection
    to the database as a dependency. Returns the result of the previous request to the external API as JSON.
    """
    return await request_my(data, db)
