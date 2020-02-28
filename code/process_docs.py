
from pymongo import MongoClient
import numpy as np
import pandas as pd
import re
from collections import defaultdict

#from example_doc import EXAMPLE_DOC

from get_docs import *




TOKENS = ['__INTEGER__', '__DECIMAL__', '__MATH__' '__STOP__',
    '__PERIOD__', '__QMARK__', '__EPOINT__', '__COMMA__'
]







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





integer_re = re.compile('\d+')
decimal_re = re.compile('\d*.\d+')
newline_re = re.compile('\n')






# to implement
def validate_word_v0(w, doc, req_freq=5):
    # first letter capitalized and in words
    if w[0].lower()+w[1:] in words: return True
    # all uppercase letters or periods
    if all(c in ascii_uppercase+'.' for c in w): return True
    # actually... given previous statement this is redundant (remove previous?)
    if all(c in ascii_uppercase for c in w) and w.lower() in words: return True
    # hyphenated and all components are words
    if all(subw in words for subw in w.split('-')): return True
    # if word appears more than req_freq times in the document
    if doc.count(w) >= req_freq: return True
    # if the word is a token (currently not used)
    if w in TOKENS: return True
    return False


def validate_word_v1(w, doc, req_freq=5):
    pass    


def preprocess_docs(docs):
    #docs = [digits_re.sub('', dt) for dt in docs]
    docs = [newline_re.sub(' ', dt) for dt in docs]
    docs_filtered = [' '.join(w for w in d.split() if w in words or validate_word_v0(w, d)) for d in docs] 
    return docs_filtered