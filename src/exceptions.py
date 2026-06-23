from datetime import date

from fastapi import HTTPException


class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"

class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Похожий объект уже существует"

class UserAlreadyExistsException(NabronirovalException):
    detail = "Пользователь уже существует"


class EmailNotRegisteredException(NabronirovalException):
    detail="Такой email не зарегистрирован"

class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"

class RoomNotFoundException(NabronirovalException):
    detail = "Номер не найден"

class IncorrectPasswordException(NabronirovalException):
    detail = "Неверный пароль"

class HotelNotFoundException(NabronirovalException):
    detail = "Отель не найден"

def check_date_to_after_date_from(date_to: date, date_from: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Дата заезда не может быть раньше даты выезда")


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)

class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"

class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class UserEmailAlreadyExistsHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Почта уже существует"


class EmailNotRegisteredHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Почта не зарегистрирована"

class IncorrectPasswordHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Неверный пароль"


class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Номеров нет"