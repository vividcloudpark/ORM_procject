import pymysql
import pandas as pd
from sqlalchemy import create_engine
from models import *
from sqlalchemy.orm import sessionmaker


def query_all(stock_name):
    curs = cursor()
    sql = f''' SELECT * FROM StockInfo where stock_name = "{stock_name}" '''
    a = curs.execute(sql)
    result = curs.fetchall()
    print(result)

def query_by_date(stock_name, startdate, enddate):
    return

def update_stock(stock_name):
    return

def cursor():
    json_data=open("config.json").read()
    data = json.loads(json_data)

    host = data['host']
    id = data["db_id"]
    pw = data['db_password']
    db_name = data['db_name']

    engine_target = f'mysql+pymysql://{id}:{pw}@{host}/{db_name}?charset=utf8'
    engine = create_engine(engine_target, encoding='utf-8')

    Session = sessionmaker(bind=engine)
    session = Session()

    conn = pymysql.connect(host='localhost', port=3306, user=id, password=pw, use_unicode=True, charset='utf8')
    conn.cursor().execute('USE %s' %db_name)
    return conn.cursor()
