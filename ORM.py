import datetime

import psycopg2
import json
from psycopg2 import Error
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale


Base = declarative_base()

#загрузка таблиц БД из json
def add_tables(engine, json_adress):
    with open(json_adress, 'r') as fd:
        data = json.load(fd)

    for record in data:
        model = {
            'publisher': Publisher,
            'shop': Shop,
            'book': Book,
            'stock': Stock,
            'sale': Sale,
        }[record.get('model')]

        session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()
    print('Данные загружены')


#получение данных из БД
def info_tables (engine, Publisher_name=None):
    if Publisher_name.isdigit() != True:
        subq = session.query(Book.title, Stock.id, Stock.id_shop).join(Publisher).join(Stock).\
                filter(Publisher.name == Publisher_name).subquery()
        q = session.query(subq.c.title, Shop.name, Sale.price, Sale.date_sale).join(subq, Shop.id == subq.c.id_shop).\
                join(Sale, Sale.id_stock == subq.c.id).all()
        for title, name, price, data_sale in q:
            print(f'{title:<40} |  {name:<10} | {price:<5} | {data_sale}')
    else:
        subq = session.query(Book.title, Stock.id, Stock.id_shop).join(Publisher).join(Stock).\
                filter(Publisher.id == Publisher_name).subquery()
        q = session.query(subq.c.title, Shop.name, Sale.price, Sale.date_sale).join(subq, Shop.id == subq.c.id_shop).\
                join(Sale, Sale.id_stock == subq.c.id).all()
        for title, name, price, data_sale in q:
            print(f'{title:<40} |  {name:<10} | {price:<5} | {data_sale}')


try:
    DSN = "postgresql://postgres:pasword@localhost:5432/books_shop"
    engine = sqlalchemy.create_engine(DSN)
    Session = sessionmaker(bind=engine)
    session = Session()

    if __name__ == '__main__':
        create_tables(engine)
        add_tables(engine, json_adress='fixtures.json')
        info_tables(engine, input('Введи автора: '))

except (Exception, Error):
    print('Error!!', Error)
finally:

    session.close()
    print('Сессия завершена')



