from bottle import (
    route, run, template, request, redirect
)

from scrapper import get_news
from db import News, session
from bayes import NaiveBayesClassifier


@route("/")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    id = request.query.id
    label = request.query.label
    print(id, label)
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    s = session()
    row = s.query(News).filter(News.id == id).one()
    # 3. Изменить значение метки записи на значение label
    row.label = label
    # 4. Сохранить результат в БД
    s.commit()
    redirect("/")


@route("/update")
def update_news():
    s = session()
    news_list = get_news("https://news.ycombinator.com/newest")
    for news in news_list:
        if len(s.query(News).filter(News.title == news["title"], News.author == news['author']).all()) == 0:
            row = News(title=news['title'], author=news['author'], url=news['url'], comments=news['comments'], points=news['points'])
            s.add(row)
            s.commit()
    redirect("/")


@route("/classify")
def classify_news():
    s = session()
    X_train = [news.title for news in s.query(News).filter(News.label != None)]
    y_train = [news.label for news in s.query(News).filter(News.label != None)]
    model = NaiveBayesClassifier()
    model.fit(X_train, y_train)
    no_label = s.query(News).filter(News.label == None)
    X = [news.title for news in no_label]
    y = model.predict(X)
    good, maybe, never = [], [], []
    for i, label in enumerate(y):
        if label == 'good':
            good.append(no_label[i])
        elif label == 'maybe':
            maybe.append(no_label[i])
        elif label == 'never':
            never.append(no_label[i])
    return template('news_recommendations', good=good, maybe=maybe, never=never)


if __name__ == "__main__":
    run(host="localhost", port=8080)
