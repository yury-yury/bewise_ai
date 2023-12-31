from fastapi import FastAPI, APIRouter

from api.handlers import question_router


app = FastAPI(title='Test task from Bewise.ai')

main_api_router = APIRouter()
main_api_router.include_router(question_router, prefix='/quest', tags=['quest'])

app.include_router(main_api_router)
