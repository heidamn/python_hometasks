import requests
from bs4 import BeautifulSoup
import time


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    tbl_list = parser.table.findAll('table')
    posts = tbl_list[1].findAll("tr", attrs={'class': 'athing'})
    postsinfo = tbl_list[1].findAll("tr", attrs={'class': ''})
    for i in range(30):
        comment = postsinfo[i].findAll('a')[-1].text.split(' ')
        if len(comment) == 1:
            comment = 0
        else:
            comment = int(comment[0])
        post = {
            'author': postsinfo[i].findAll('a', attrs={'class': 'hnuser'})[0].text,
            'comments': comment,
            'points': int(postsinfo[i].findAll('span', attrs={'class': 'score'})[0].text.split(' ')[0]),
            'title': posts[i].findAll('a')[1].text,
            'url': posts[i].findAll('a', attrs={'class': 'storylink'})[0]['href']
        }
        news_list.append(post)
    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    tbl_list = parser.table.findAll('table')
    next_page = tbl_list[1].findAll("tr", attrs={'class': ''})[30].a['href']
    return next_page


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        time.sleep(30)
    return news

