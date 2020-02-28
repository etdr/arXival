
import numpy as np
import pandas as pd

from pymongo import MongoClient

MONTHS = ['19'+str(m).zfill(2) for m in range(1,13)]

client = MongoClient()
db = client.arXiv


c1901 = db['1901']
c1902 = db['1902']
c1903 = db['1903']
c1904 = db['1904']
c1905 = db['1905']
c1906 = db['1906']
c1907 = db['1907']
c1908 = db['1908']
c1909 = db['1909']
c1910 = db['1910']
c1911 = db['1911']
c1912 = db['1912']


def get_docs_by_month(month, field='text'):
    return [d[field] for d in db[month].find({})]

def get_docs(months=MONTHS, field='text'):
    docs_by_month = [get_docs_by_month(m, field=field) for m in months]
    return [d for m in docs_by_month for d in m]