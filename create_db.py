import pymysql
import json
from sqlalchemy import create_engine
from models import *
from sqlalchemy.orm import sessionmaker
import pandas as pd

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
try:
    conn.cursor().execute('create database %s' %db_name)
    conn.cursor().execute('USE %s' %db_name)
    Base.metadata.create_all(engine)

    KOSPI = pd.read_excel("basic.xls", sheet_name=0, encoding='utf8')
    KOSDAQ = pd.read_excel("basic.xls", sheet_name=1, encoding='utf8')
    KOSPI.종목코드 = KOSPI.종목코드.map('{:06d}'.format)
    KOSDAQ.종목코드 = KOSDAQ.종목코드.map('{:06d}'.format)

    KOSPI = KOSPI.to_dict()
    KOSDAQ = KOSDAQ.to_dict()

    for i in range(len(KOSPI['기업명'])):
        temp = StockInfo(str(KOSPI["종목코드"][i]), KOSPI["기업명"][i], "KOSPI")
        session.add(temp)
    for i in range(len(KOSDAQ['기업명'])):
        temp = StockInfo(str(KOSDAQ["종목코드"][i]), KOSDAQ["기업명"][i], "KOSDAQ")
        session.add(temp)

    session.commit()
    session.close()

except:
    print("이미 DB가 생성되어 있습니다. 삭제후 다시 실행해주세요")
