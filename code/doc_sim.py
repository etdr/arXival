
from collections import defaultdict
from typing import Iterator
import pickle
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .get_docs import get_docs_list_from_dict, get_docs_list_iter, get_docs_dict_iter, get_doc_str

MONTHS = ['1901', '1902']

cossim = lambda x, y: dot(x, y) / (norm(x) * norm(y))



# use get_docs_dict function with "text_dtr" as field argument




def get_tfidf_vectorizer_and_fit(ddi:Iterator[dict]=None, max_df=0.4, min_df=3, field='text_dtr'):
    if ddi is None:
        ddi = get_docs_dict_iter(months=MONTHS)
    docs_list = get_docs_list_iter(ddi, field=field)
    v = TfidfVectorizer(max_df=max_df, min_df=min_df)
    v.fit(docs_list)
    return v


def save_vectorizer(v):
    with open('v.pickle', 'wb') as f:
        pickle.dump(v, f)
    return

def load_vectorizer():
    with open('v.pickle', 'rb') as f:
        v = pickle.load(f)
    return v


LOAD_VECTORIZER = True

if LOAD_VECTORIZER:
    v = load_vectorizer()


def get_tfidf_array(dd, v):
    return v.transform()


def cssim_rank(doc_str, v:TfidfVectorizer=v, ddi:Iterator[dict]=None, doc_str_from_corpus=True, n=10, field='text_dtr'):
    if ddi is None:
        ddi = get_docs_dict_iter(months=MONTHS)
    doc0_vec = v.transform([doc_str])
    doc_results = list()
    for doc1 in ddi:
        #doc1r = doc1.copy()
        if field not in doc1:
            continue
        doc1b = dict()
        doc1b['aID'] = doc1['aID']
        doc1b['date'] = doc1['date']
        doc1b['subjects'] = doc1['subjects']
        doc1b['cssim'] = cosine_similarity(doc0_vec, v.transform([doc1[field]]))[0][0]
        doc_results.append(doc1b)
    doc_results.sort(key=lambda d: d['cssim'], reverse=True)
    if doc_str_from_corpus:
        return doc_results[1:n+1]
    else:
        return doc_results[:n]