from collections import Counter
import datetime
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from typing import List, Tuple

from api import messages_get_history
from api_models import Message
import config


Dates = List[datetime.date]
Frequencies = List[int]


plotly.tools.set_credentials_file(
    username=config.PLOTLY_CONFIG['username'],
    api_key=config.PLOTLY_CONFIG['api_key']
)


def fromtimestamp(ts: int) -> datetime.date:
    return datetime.datetime.fromtimestamp(ts).date()


def count_dates_from_messages(messages: List[Message]) -> Tuple[Dates, Frequencies]:
    """ Получить список дат и их частот

    :param messages: список сообщений
    """
    dates = []
    messn = []
    for message in messages['response']['items']:
        date = datetime.datetime.fromtimestamp(message['date']).strftime("%Y-%m-%d")
        try:
            messn[dates.index(date)] += 1
        except:
            dates.append(date)
            messn.append(1)
    dates.reverse()
    messn.reverse()
    message_count = (dates, messn)
    return message_count


def plotly_messages_freq(dates: Dates, freq: Frequencies) -> None:
    """ Построение графика с помощью Plot.ly

    :param date: список дат
    :param freq: число сообщений в соответствующую дату
    """
    # PUT YOUR CODE HERE
