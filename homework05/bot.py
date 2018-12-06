import requests
import config
import telebot
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
    print(message.text)
    try:
        day, group, week = message.text.split()
    except:
        week = '0'
        day, group = message.text.split()
    days = {'/monday': '1day', '/tuesday': '2day', '/wednesday': '3day', '/thursday': '4day', '/friday': '5day', '/saturday': '6day', '/sunday': '7day'}
    web_page = get_page(group)
    day = days[day]
    soup = BeautifulSoup(web_page, "html5lib")
    # Получаем таблицу с расписанием на день
    schedule_table = soup.find("table", attrs={"id": day})
    if not schedule_table:
        bot.send_message(message.chat.id, 'День свободен!')
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
        resp = ''
        for time, location, room, lession in zip(times_list, locations_list, rooms_list, lessons_list):
            if week == '0':
                resp += '<b>{}</b>, {}, {} {}\n'.format(time, location, room, lession)
            elif week == '1':
                if lession.find('нечетная неделя') != -1:
                    resp += '<b>{}</b>, {},{} {}\n'.format(time, location, room, lession)
            else:
                if lession.find('нечетная неделя') == -1:
                    resp += '<b>{}</b>, {},{} {}\n'.format(time, location, room, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    # PUT YOUR CODE HERE
    pass


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    
    pass


if __name__ == '__main__':
    bot.polling(none_stop=True)

