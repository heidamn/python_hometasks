from typing import List, Optional
from pydantic import BaseModel


class BaseUser(BaseModel):
    """ Модель пользователя с базовыми полями """
    id: int
    first_name: str
    last_name: str
    online: int


class User(BaseUser):
    """ Модель пользователя с необязательным полем дата рождения """
    bdate: Optional[str]


class Message(BaseModel):
    """ Модель сообщения """
    text: str
    date: int

