import requests
import config
import telebot
from time import sleep
from datetime import datetime, timedelta, time as Time
from bs4 import BeautifulSoup


bot = telebot.TeleBot(config.access_token)


def get_page(group, week=0):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def lists_creator(schedule_table):
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
    return times_list, locations_list, lessons_list, rooms_list


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
        bot.send_message(message.chat.id, "Аргументы:\ngroup_number - номер группы\nweek - номер недели(0 - все недели, 1 - четн, 2 - нечетн)")
        return None
    if week not in [0, 1, 2]:
        week = week % 2
        if week == 0:
            week = 2
    if day.find('@heidamn_itmo_bot') != -1:
        day = day[:-17]
    days = {'/monday': '1day', '/tuesday': '2day', '/wednesday': '3day', '/thursday': '4day', '/friday': '5day', '/saturday': '6day', '/sunday': '7day'}
    days2 = {'/monday': 'Понедельник', '/tuesday': 'Вторник', '/wednesday': 'Среда', '/thursday': 'Четверг', '/friday': 'Пятница', '/saturday': 'Суббота', '/sunday': 'Воскресенье'}
    web_page = get_page(group, week=week)
    day, day2 = days[day], days2[day]
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на день
    schedule_table = soup.find("table", attrs={"id": day})
    if not schedule_table:
        bot.send_message(message.chat.id, '<b>{}</b>\n\nДень свободен!'.format(day2), parse_mode='HTML')
    else:
        times_list, locations_list, rooms_list, lessons_list = lists_creator(schedule_table)
        resp = '<b>{}\n\n</b>'.format(day2)
        for time, location, room, lession in zip(times_list, locations_list, rooms_list, lessons_list):
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
    today = datetime.fromtimestamp(message.date)
    if today.month >= 9:
        first_sept = datetime(today.year, 9, 1)
        first_sept = first_sept - timedelta(first_sept.weekday())
    else:
        first_sept = datetime(today.year-1, 9, 1)
        first_sept = first_sept - timedelta(first_sept.weekday())
    week = ((today - first_sept).days // 7 + 1) % 2
    if week == 0:
        week = 2
    web_page = get_page(group, week=week)
    soup = BeautifulSoup(web_page, "html5lib")
    for _n in range(14):
        now = Time(today.hour, today. minute)
        if today.weekday() == 0:
            if week == 2:
                week = 1
                web_page = get_page(group, week)
                soup = BeautifulSoup(web_page, "html5lib")
            else:
                week = 2
                web_page = get_page(group, week)
                soup = BeautifulSoup(web_page, "html5lib")
        schedule_table = soup.find("table", attrs={"id": days[today.weekday()]})
        times_list_Time = []
        if schedule_table:
            times_list, locations_list, rooms_list, lessons_list = lists_creator(schedule_table)
            for time in times_list:
                if time != 'День':
                    time = time.split('-')
                    time = time[0].split(':')
                    times_list_Time.append(Time(int(time[0]), int(time[1])))
                else:
                    times_list_Time.append(Time(23, 59))
            for time, location, room, lession, time_Time in zip(times_list, locations_list, rooms_list, lessons_list, times_list_Time):
                if week == 1 and time_Time >= now:
                    resp = '<b>{}\n\n{}</b>, {},{} {}\n'.format(days2[today.weekday()], time, location, room, lession)
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    return None
                elif time_Time >= now:
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
        bot.send_message(message.chat.id, "Аргументы:\ngroup_number - номер группы\nweek - номер недели(0 - все недели, 1 - четн, 2 - нечетн)")
        return None
    if week not in [0, 1, 2]:
        week = week % 2
        if week == 0:
            week = 2
    days = ['1day', '2day', '3day', '4day', '5day', '6day', '7day']
    days2 = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    web_page = get_page(group, week=week)
    soup = BeautifulSoup(web_page, "html5lib")
    for num, day in enumerate(days):
        # Получаем таблицу с расписанием на день
        schedule_table = soup.find("table", attrs={"id": day})
        if not schedule_table:
            bot.send_message(message.chat.id, '<b>{}</b>\n\nДень свободен!'.format(days2[num]), parse_mode='HTML')
        else:
            resp = '<b>{}</b>\n\n'.format(days2[num])
            times_list, locations_list, rooms_list, lessons_list = lists_creator(schedule_table)
            for time, location, room, lession in zip(times_list, locations_list, rooms_list, lessons_list):
                resp += '<b>{}</b>, {}  ,{} {}\n'.format(time, location, room, lession)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, """
    <b>Commands:
      monday - sunday:</b>
           arguments:
             group_number - номер группы
             week - номер недели(0 - все недели, 1 - четн, 2 - нечетн)
           example:
             /wednesday k3120 1
      <b>all:</b>
           arguments:
             group_number - номер группы
             week - номер недели(0 - все недели, 1 - четн, 2 - нечетн)
           example:
             /all m4245 2
      <b>near:</b>
           arguments:
             group_number - номер группы
           example:
             /near k3140
      <b>tomorrow:</b>
           arguments:
             group_number - номер группы
           example:
             /tomorrow k3120 1
    """, parse_mode='HTML')


@bot.message_handler(commands=['hi_shakal'])
def shakal(message):
    shakal = """⠀
⠀⠀⠀⠀435⠀⠀⠀⠀⠀4235⠀
⠀⠀⠀43335⠀⠀⠀⠀43525⠀
⠀⠀⠀35935⠀⠀⠀⠀35527⠀
⠀⠀⠀12559649599537⠀⠀
⠀⠀⠀⠀5088054953362⠀⠀
⠀⠀⠀33805⠀085⠀80335⠀
⠀⠀53358365830933357⠀
⠀⠀⠀333548⠀⠀033335⠀⠀45352
⠀⠀⠀⠀93530⠀333350⠀⠀445454
⠀⠀⠀⠀⠀2038⠀53639960695637
⠀⠀⠀⠀⠀43344033355454537⠀
⠀⠀⠀⠀4333666633334650⠀
⠀⠀⠀443555553395399456
⠀⠀⠀0530339449593643452⠀
⠀⠀⠀436⠀335⠀⠀⠀⠀⠀9403349
⠀⠀⠀630⠀⠀54⠀⠀⠀⠀⠀650⠀⠀33
⠀⠀⠀535⠀⠀239⠀⠀⠀⠀630⠀⠀59
⠀⠀7333⠀⠀736⠀⠀⠀⠀530⠀⠀33
⠀⠀933⠀⠀⠀33⠀⠀⠀⠀⠀336⠀⠀33⠀
⠀⠀333⠀333⠀⠀⠀⠀⠀⠀335⠀⠀⠀533
55537⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀93333
⠀⠀⠀⠀⠀⠀⠀HI_HUMAN⠀⠀⠀⠀⠀⠀
"""
    bot.send_message(message.chat.id, shakal)

if __name__ == '__main__':
    bot.polling(none_stop=True)

