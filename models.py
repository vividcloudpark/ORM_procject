# -*- coding: utf-8 -*-
import pymysql
import sqlalchemy as sa
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()



class StockInfo(Base):
    __tablename__ = 'StockInfo'

    stock_code = sa.Column(sa.String(10), nullable=False, primary_key=True)
    stock_name = sa.Column(sa.String(200), nullable=True)
    stock_market = sa.Column(sa.String(10), nullable=True)

    def __init__(self, stock_code, stock_name, stock_market):
        self.stock_code = stock_code
        self.stock_name = stock_name
        self.stock_market = stock_market

class StockHistory(Base):
    __tablename__ = 'StockHistory'

    stock_code = sa.Column(sa.String(10), nullable=False, primary_key=True)
    basic_date = sa.Column(sa.Date, nullable=False, primary_key=True)
    open_value = sa.Column(sa.Float, nullable=True)
    high_value = sa.Column(sa.Float, nullable=True)
    low_value = sa.Column(sa.Float, nullable=True)
    close_value = sa.Column(sa.Float, nullable=True)
    volume_value = sa.Column(sa.Float, nullable=True)
    sa.UniqueConstraint('stock_code', 'basic_date', name='StockHistoryUnique')
    sa.PrimaryKeyConstraint('stock_code', 'basic_date')

    def __init__(self, stock_code, basic_date, open_value, high_value,\
    low_value, close_value, volume_value):
        self.stock_code = stock_code
        self.basic_date = basic_date
        self.open_value = open_value
        self.high_value = high_value
        self.low_value = low_value
        self.close_value = close_value
        self.volume_value = volume_value
