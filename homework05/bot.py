import requests
import config
import telebot
from time import sleep
from datetime import datetime, timedelta, time as Time
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    parts = message.text.split()
    if len(parts) == 3:
        day, group, week = parts
        week = int(week)
    elif len(parts) == 2:
        week = 0
        day, group = parts
    else:
        bot.send_message(message.chat.id, "Аргументы:\ngroup_number - номер группы\nweek - номер недели(0 - все недели, 1 - нечетн, 2 - четн)")
        return None
    if week not in [0, 1, 2]:
        week = week % 2
        if week == 0:
            week = 2
    if day.find('@heidamn_itmo_bot') != -1:
        day = day[:-17]
    days = {'/monday': '1day', '/tuesday': '2day', '/wednesday': '3day', '/thursday': '4day', '/friday': '5day', '/saturday': '6day', '/sunday': '7day'}
    days2 = {'/monday': 'Понедельник', '/tuesday': 'Вторник', '/wednesday': 'Среда', '/thursday': 'Четверг', '/friday': 'Пятница', '/saturday': 'Суббота', '/sunday': 'Воскресенье'}
    web_page = get_page(group)
    day, day2 = days[day], days2[day]
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на день
    schedule_table = soup.find("table", attrs={"id": day})
    if not schedule_table:
        bot.send_message(message.chat.id, '<b>{}</b>\n\nДень свободен!'.format(day2), parse_mode='HTML')
    else:
        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]
        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]
        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
        # Аудитория
        rooms_list = schedule_table.find_all("td", attrs={"class": "room"})
        rooms_list = [room.dd.text for room in rooms_list]
        resp = '<b>{}\n\n</b>'.format(day2)
        for time, location, room, lession in zip(times_list, locations_list, rooms_list, lessons_list):
            if week == 0:
                resp += '<b>{}</b>, {},{} {}\n'.format(time, location, room, lession)
            elif week == 1:
                if lession.find('нечетная неделя') != -1 or lession.find('четная неделя') == -1:
                    resp += '<b>{}</b>, {},{} {}\n'.format(time, location, room, lession)
            else:
                if lession.find('нечетная неделя') == -1:
                    resp += '<b>{}</b>, {},{} {}\n'.format(time, location, room, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    parts = message.text.split()
    if len(parts) == 2:
        _, group = parts
    else:
        bot.send_message(message.chat.id, "Аргументы:\ngroup_number - номер группы")
        return None
    days = ['1day', '2day', '3day', '4day', '5day', '6day', '7day']
    days2 = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    web_page = get_page(group)
    today = datetime.fromtimestamp(message.date)
    soup = BeautifulSoup(web_page, "html5lib")
    if today.month >= 9:
        first_sept = datetime(today.year, 9, 1)
    else:
        first_sept = datetime(today.year-1, 9, 1)
    for _n in range(10):
        now = Time(today.hour, today. minute)
        week = (today - first_sept).days // 7 % 2
        if week == 0:
            week = 2
        schedule_table = soup.find("table", attrs={"id": days[today.weekday()]})
        if schedule_table:
            # Время проведения занятий
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            times_list = [time.span.text for time in times_list]
            times_list_Time=[]
            for time in times_list:
                if time != 'День':
                    time = time.split('-')
                    time = time[0].split(':')
                    times_list_Time.append(Time(int(time[0]), int(time[1])))
                else:
                    times_list_Time.append(Time(23,59))
            #  Место проведения занятий
            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            locations_list = [room.span.text for room in locations_list]
            # Название дисциплин и имена преподавателей
            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
            lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
            # Аудитория
            rooms_list = schedule_table.find_all("td", attrs={"class": "room"})
            rooms_list = [room.dd.text for room in rooms_list]
            for time, location, room, lession, time_Time in zip(times_list, locations_list, rooms_list, lessons_list, times_list_Time):
                if week == 1:
                    if lession.find('нечетная неделя') != -1 or lession.find('четная неделя') == -1 and time_Time >= now:
                        resp = '<b>{}\n\n{}</b>, {},{} {}\n'.format(days2[today.weekday()], time, location, room, lession)
                        bot.send_message(message.chat.id, resp, parse_mode='HTML')
                        return None
                elif time_Time >= now:
                    if lession.find('нечетная неделя') == -1:
                        resp = '<b>{}\n\n{}</b>, {},{} {}\n'.format(days2[today.weekday()], time, location, room, lession)
                        bot.send_message(message.chat.id, resp, parse_mode='HTML')
                        return None
        today = today.replace(hour=0, minute=0, second=0)
        today = today + timedelta(1)
    else:
        bot.send_message(message.chat.id, 'Ошибка расписания на сайте ИТМО!!!')


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    parts = message.text.split()
    if len(parts) == 2:
        _, group = parts
    else:
        bot.send_message(message.chat.id, "Аргументы:\ngroup_number - номер группы")
        return None
    today = datetime.fromtimestamp(message.date)
    tomorrow = today + timedelta(1)
    days = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    if today.month >= 9:
        first_sept = datetime(today.year, 9, 1)
    else:
        first_sept = datetime(today.year-1, 9, 1)
    week = (tomorrow - first_sept).days // 7 % 2
    if week == 0:
        week = 2
    message.text = '{} {} {}'.format(days[tomorrow.weekday()], group, week)
    get_schedule(message)


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    parts = message.text.split()
    if len(parts) == 3:
        day, group, week = parts
        week = int(week)
    elif len(parts) == 2:
        week = 0
        day, group = parts
    else:
        bot.send_message(message.chat.id, "Аргументы:\ngroup_number - номер группы\nweek - номер недели(0 - все недели, 1 - нечетн, 2 - четн)")
        return None
    if week not in [0, 1, 2]:
        week = week % 2
        if week == 0:
            week = 2
    days = ['1day', '2day', '3day', '4day', '5day', '6day', '7day']
    days2 = ['Понедельник','Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    web_page = get_page(group)
    soup = BeautifulSoup(web_page, "html5lib")
    for num, day in enumerate(days):
        # Получаем таблицу с расписанием на день
        schedule_table = soup.find("table", attrs={"id": day})
        if not schedule_table:
            bot.send_message(message.chat.id, '<b>{}</b>\n\nДень свободен!'.format(days2[num]), parse_mode='HTML')
        else:
            # Время проведения занятий
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            times_list = [time.span.text for time in times_list]
            # Место проведения занятий
            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            locations_list = [room.span.text for room in locations_list]
            # Название дисциплин и имена преподавателей
            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
            lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
            # Аудитория
            rooms_list = schedule_table.find_all("td", attrs={"class": "room"})
            rooms_list = [room.dd.text for room in rooms_list]
            resp = '<b>{}</b>\n\n'.format(days2[num])
            for time, location, room, lession in zip(times_list, locations_list, rooms_list, lessons_list):
                if week == 0:
                    resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, room, lession)
                elif week == 1:
                    if lession.find('нечетная неделя') != -1 or lession.find('четная неделя') == -1:
                        resp += '<b>{}</b>, {},{} {}\n'.format(time, location, room, lession)
                else:
                    if lession.find('нечетная неделя') == -1:
                        resp += '<b>{}</b>, {},{} {}\n'.format(days2[num], time, location, room, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')



if __name__ == '__main__':
    bot.polling(none_stop=True)

