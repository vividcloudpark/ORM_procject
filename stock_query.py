import pymysql
import pandas as pd
from sqlalchemy import create_engine
from models import *
from sqlalchemy.orm import sessionmaker
import urllib
import datetime

def get_stock_code(stock_name):
    curs = cursor()
    try:
        sql = f''' SELECT * FROM StockInfo where stock_name = "{stock_name}" '''
        a = curs.execute(sql)
        result = curs.fetchone()
        curs.close()
        return result
    except:
        print("이름을 확인해주세요")

def query_all(stock_name):
    result = get_stock_code(stock_name)
    stock_number = result[0]

    curs = cursor()
    search = f'''SELECT * FROM StockHistory Where stock_code = "{stock_number}"'''
    try:
        a = curs.execute(search)
        sqlresult = curs.fetchall()
        curs.close()
        if sqlresult != None:
            curs = cursor()
            delete = f'''DELETE FROM stockhistory WHERE stock_code = "{stock_number}"'''
            a = curs.execute(delete)
            curs.close()
            print("초기화완료!")
            print("다시 데이터를 삽입합니다")
    except:
        pass

    else:
        print("데이터를 다운로드합니다")

    eddate = datetime.date.today().strftime('%b+%d+%Y')
    symbol = f'q=KRX:{stock_number}&'
    stdate='startdate=Jan+01+2000&'
    eddate=f'enddate={eddate}&'
    outtype= 'output=csv'

    target = f'https://finance.google.co.uk/bctzjpnsun/historical?{symbol}{stdate}{eddate}{outtype}'
    print(target)
    tempcsv = urllib.request.urlretrieve(target, 'temp.csv')
    result = pd.read_csv(tempcsv[0])


    put_in_lovesong(stock_number, result)
    return result

def query_by_date(stock_name, startdate, enddate):
    result = get_stock_code(stock_name)
    stock_number = result[0]
    pystdate = datetime.datetime.strptime(startdate, '%b-%d-%Y').date()
    pyeddate = datetime.datetime.strptime(enddate, '%b-%d-%Y').date()
    stdate = pystdate.strftime('%b+%d+%y')
    eddate = pyeddate.strftime('%b+%d+%y')

    try:
        curs = cursor()
        sqlstdate = pystdate.strftime('%Y-%m-%d')
        sqleddate = pyeddate.strftime('%Y-%m-%d')
        istheredata = f'''SELECT * FROM stockhistory
        WHERE
        stock_code = '{stock_number}'
        AND
        (basic_date BETWEEN '{sqlstdate}' AND '{sqleddate}')
        '''
        a = curs.execute(istheredata)
        sqlresult = curs.fetchall()
        curs.close()
    except:
        pass

    if sqlresult != None:
        curs = cursor()
        delete = f'''DELETE FROM stockhistory
        WHERE
        stock_code = '{stock_number}'
        AND
        (basic_date BETWEEN '{sqlstdate}' AND '{sqleddate}')'''
        a = curs.execute(delete)
        curs.close()
        print("삭제완료!")
    else:
        print("삭제할 데이터가 없습니다")
    print("데이터를 다운로드합니다")

    symbol = f'q=KRX:{stock_number}&'
    stdate=f'startdate={stdate}&'
    eddate=f'enddate={eddate}&'
    outtype= 'output=csv'

    target = f'https://finance.google.co.uk/bctzjpnsun/historical?{symbol}{stdate}{eddate}{outtype}'
    tempcsv = urllib.request.urlretrieve(target, 'temp.csv')
    result = pd.read_csv(tempcsv[0])

    put_in_lovesong(stock_number, result)
    return result



def update_stock(stock_name):
    result = get_stock_code(stock_name)
    stock_number = result[0]
    try:
        curs = cursor()
        sql = f''' SELECT * FROM StockHistory
        where stock_code = "{stock_number}"
        ORDER BY basic_date DESC'''
        a = curs.execute(sql)
        result = curs.fetchall()
        curs.close()
        if result == None:
            print("에러!! 이전에 다운로드된 데이터가 없습니다. query_all을 이용해주세요")
            return
    except:
        print("무언가가 잘못된것 같아요...")

    stdate = result[0][1].strftime('%b+%d+%Y')
    eddate = datetime.date.today().strftime('%b+%d+%Y')

    symbol = f'q=KRX:{stock_number}&'
    stdate=f'startdate={stdate}&'
    eddate=f'enddate={eddate}&'
    outtype= 'output=csv'

    target = f'https://finance.google.co.uk/bctzjpnsun/historical?{symbol}{stdate}{eddate}{outtype}'
    tempcsv = urllib.request.urlretrieve(target, 'temp.csv')
    result = pd.read_csv(tempcsv[0])

    put_in_lovesong(stock_number, result)

    print("업데이트된 결과입니다")
    return result



def mk_session():
    json_data=open("config.json").read()
    data = json.loads(json_data)

    host = data['host']
    id = data["db_id"]
    pw = data['db_password']
    db_name = data['db_name']

    engine_target = f'mysql+pymysql://{id}:{pw}@{host}/{db_name}?charset=utf8'
    engine = create_engine(engine_target, encoding='utf-8')

    Session = sessionmaker(bind=engine)
    return Session()

def put_in_lovesong(stock_number, result):
    stockdict = result.to_dict()
    session = mk_session()
    try:
        for i in range(len(stockdict['Date'])):
            date = stockdict['Date'][i]
            input_date = datetime.datetime.strptime(date, '%d-%b-%y').date()
            values = StockHistory(stock_number, input_date, stockdict[' Open'][i], stockdict[' High'][i],\
            stockdict[' Low'][i], stockdict[' Close'][i], stockdict[' Volume'][i])
            session.merge(values)
        session.commit()
    except:
        print("앗! 에러발생! 다시실행해주세요")
    finally:
        session.close()


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
