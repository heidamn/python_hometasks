from datetime import date
from statistics import median
from typing import Optional

from api import get_friends
from api_models import User


def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей
    Возраст считается как медиана среди возраста всех друзей пользователя
    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """

    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    friends = get_friends(user_id, "bdate")
    age_list = []
    for friend in friends:
        try:
            bdate = friend['bdate']
            if len(bdate) >= 8:
                age_list.append(bdate)
        except:
                pass
    for pos, age in enumerate(age_list):
        age = age.split('.')
        bdate = date(int(age[2]), int(age[1]), int(age[0]))
        today = date.today()
        age_list[pos] = today.year - bdate.year - ((today.month, today.day) < (bdate.month, bdate.day))
    age_list.sort()
    if len(age_list) % 2 == 0 and len(age_list) != 0:
        return (age_list[len(age_list)//2 -1] + age_list[len(age_list)//2]) / 2
    elif len(age_list) == 0:
        return None
    else:
        return age_list[len(age_list)//2]
