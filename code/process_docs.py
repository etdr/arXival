
from pymongo import MongoClient
import numpy as np
import pandas as pd
from collections import defaultdict

from example_doc import EXAMPLE_DOC


MONTHS = ['19'+str(m).zfill(2) for m in range(1,13)]



def count_subjects(docs):
    dd = defaultdict(int)
    for doc in docs:
        for s in doc['subjects']:
            dd[s] += 1
    return dd

def combine_dds(dds):
    masterdd = defaultdict(int)
    for dd in dds:
        for topic in dd.keys():
            masterdd[topic] += dd[topic]
    return masterdd

def count_and_combine_dds(db):
    master = defaultdict(int)
    for m in MONTHS:
        master = combine_dds([master, count_subjects(d for d in db[m])])
    return master