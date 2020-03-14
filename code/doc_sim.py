
from collections import defaultdict
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from get_docs import get_docs_list_from_dict, get_docs_list_iter, get_docs_dict_iter

MONTHS = ['1901', '1902']

cossim = lambda x, y: dot(x, y) / (norm(x) * norm(y))



# use get_docs_dict function with "text_dtr" as field argument




def get_tfidf_vectorizer_and_fit(ddi, max_df=0.4, min_df=3, field='text_dtr'):
    docs_list = get_docs_list_iter(ddi, field=field)
    v = TfidfVectorizer(max_df=max_df, min_df=min_df)
    v.fit(docs_list)
    return v



def get_tfidf_array(dd, v):
    return v.transform()


def cssim_rank(doc_str, v:TfidfVectorizer, ddi=None, n=10, field='text_dtr'):
    if ddi is None:
        ddi = get_docs_dict_iter(months=MONTHS)
    doc0_vec = v.transform([doc_str])
    cssims = list()
    for doc1 in ddi:
        cssims.append((doc1, cosine_similarity(doc0_vec, v.transform([ddi[doc1][field]]))[0][0]))
    cssims.sort(key=lambda x: x[1], reverse=True)
    return cssims[1:n+1]