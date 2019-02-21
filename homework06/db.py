from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapper import get_news

Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


def db_create(url, n_pages=1):
    s = session()
    news_list = get_news(url, n_pages=n_pages)
    for news in news_list:
        row = News(title=news['title'], author=news['author'], url=news['url'], comments=news['comments'], points=news['points'])
        s.add(row)
    s.commit()


Base.metadata.create_all(bind=engine)
