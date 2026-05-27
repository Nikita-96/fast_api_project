from fastapi import APIRouter,HTTPException, Response

from src.api.dependencies import UserIdDep, DBDep
from src.schema.users import UserRequestAdd, UserAdd
from src.service.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])

@router.post("/register", description="Регистрация пользователя")
async def register_user(
    data: UserRequestAdd,
    db: DBDep
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    try:
        await db.users.add(new_user_data)
        await db.commit()
        return {"status": "OK"}
    except Exception:
        raise HTTPException(status_code=401, detail="Пользователь с таким email уже существует")


@router.post("/login", description="Аутентификация пользователя")
async def login_user(
    data: UserRequestAdd,
    response: Response,
    db: DBDep
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    access_token = AuthService().create_access_token({"user_id": user.id})
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Неверный пароль")
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.get("/me")
async def only_auth(
        user_id: UserIdDep,
        db: DBDep
):
    user = await db.users.get_one_or_none(id=user_id)
    return user

@router.post("/logout", description="Выход пользователя")
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}


