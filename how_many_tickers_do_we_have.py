from __future__ import division
import itertools
import numpy as np
import pandas as pd # pandas
import datetime
from pyq_api import get_ticker_info
import os
from sqlalchemy import Column, ForeignKey, String, Date, Float, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from process_data import get_funds
from utils import get_quarters
from sqlalchemy.orm import sessionmaker
from sqlalchemy import UniqueConstraint

def establish_session():
    engine = create_engine('sqlite:///price_db3.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    return session

Base = declarative_base()

class Ticker(Base):
    __tablename__ = 'ticker'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), index=True)
    date = Column(Date, index=True, nullable=False)
    price = Column(Float, nullable=False)
    __table_args__ = (UniqueConstraint('name', 'date', name='_ticker_date'),)

from sqlalchemy import distinct
session = establish_session()

counts = []
print session.query(distinct(Ticker.name)).count()
#ticker = name[0]
#    counts.append((ticker, session.query(Ticker).filter(Ticker.name == ticker).count()))
#print counts