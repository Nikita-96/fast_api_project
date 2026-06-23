from fastapi import APIRouter, HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectAlreadyExistsException, UserAlreadyExistsException, \
    UserEmailAlreadyExistsHTTPException, EmailNotRegisteredException, EmailNotRegisteredHTTPException, \
    IncorrectPasswordException, IncorrectPasswordHTTPException
from src.schema.users import UserRequestAdd, UserAdd
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post("/register", description="Регистрация пользователя")
async def register_user(data: UserRequestAdd, db: DBDep):
    try:
        await AuthService(db).register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException
    return {"status": "OK"}


@router.post("/login", description="Аутентификация пользователя")
async def login_user(data: UserRequestAdd, response: Response, db: DBDep):
    try:
        access_token = await AuthService(db).login_user(data=data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def only_auth(user_id: UserIdDep, db: DBDep):
    return await AuthService(db).get_one_or_none_user(id=user_id)


@router.post("/logout", description="Выход пользователя")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}
