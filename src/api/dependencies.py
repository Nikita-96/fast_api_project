from pydantic import BaseModel
from fastapi import Depends, Query, HTTPException
from typing import Annotated
from starlette.requests import Request

from src.database import async_session_maker
from src.service.auth import AuthService
from src.utils.db_manager import DBManager


class Pages(BaseModel):
    page: Annotated[int | None, Query(1, ge=1)]
    per_page: Annotated[int | None, Query(None, ge=1, le=30)]

pagDep = Annotated[Pages, Depends()]

def get_token(request: Request) -> str:
    token = request.cookies.get("access_token", None)
    if not token:
        raise HTTPException(status_code=401,detail="Пользователь не авторизован")
    return token

def get_user_id(token: str = Depends(get_token)) -> int:
    user_dict = AuthService().decode_token(token)
    return user_dict.get("user_id")

UserIdDep = Annotated[int, Depends(get_user_id)]


async def get_db():
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


DBDep = Annotated[DBManager, Depends(get_db)]