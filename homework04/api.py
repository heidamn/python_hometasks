import requests
import time
import config
import random

def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = backoff_factor
    for tryn in range(max_retries+1):
        try:
            response = requests.get(url, params=params, timeout=timeout)
        except requests.exceptions.RequestException:
            if tryn == max_retries:
                 raise
            time.sleep(delay)
        else:
            return response
        delay = delay + delay * (backoff_factor + random.random())


def get_friends(user_id, fields):
    """ Вернуть данных о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"

    domain = "https://api.vk.com/method"
    access_token = config.VK_CONFIG['access_token']
    user_id = user_id

    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'fields': fields
    }

    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = get(query)
    return response.json()


def messages_get_history(user_id, offset=0, count=200):
    """ Получить историю переписки с указанным пользователем

    :param user_id: идентификатор пользователя, с которым нужно получить историю переписки
    :param offset: смещение в истории переписки
    :param count: число сообщений, которое нужно получить
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    domain = "https://api.vk.com/method"
    access_token = config.VK_CONFIG['access_token']
    user_id = user_id
    query_params = {
        'domain': domain,
        'access_token': access_token,
        'user_id': user_id,
        'offset': offset,
        'count': count
    }

    query = "{domain}/messages.getHistory?access_token={access_token}&user_id={user_id}&offset={offset}&count={count}&v=5.53".format(**query_params)
    response = get(query)
    return response.json()