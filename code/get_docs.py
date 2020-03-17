
from collections import defaultdict
from itertools import chain
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

def get_dicts_by_month(month, field='text'):
     return {d['aID']: defaultdict(str,
        [('subjects', d['subjects']),
        ('date', d['date'])] +
        ([(field, d[field])] if field in d else [])) for d in db[month].find({})}

def get_dict_iter_by_month(month):
    return db[month].find({})


def get_docs(months=MONTHS, field='text'):
    docs_by_month = [get_docs_by_month(m, field=field) for m in months]
    return [d for m in docs_by_month for d in m]


def get_docs_dict(months=MONTHS, field='text'):
    dicts_by_month = [get_dicts_by_month(m, field) for m in months]
    dicts = {}
    for md in dicts_by_month:
        dicts.update(md)
    return dicts

def get_docs_dict_iter(months=MONTHS):
    return chain(*[get_dict_iter_by_month(m) for m in months])

def get_docs_list_from_dict(dd, field='text', include_empty=False):
    if not include_empty:
        return [d[field] for d in dd.values() if field in d]
    if include_empty:
        raise

def get_docs_list_iter(ddi, field='text', include_empty=False):
    for d in ddi:
        if field in d:
            yield d[field]
        else:
            continue



def get_doc_str(aID, field='text'):
    cname = aID.split('.')[0]
    c = db[cname]

    return c.find_one({'aID':aID})[field]