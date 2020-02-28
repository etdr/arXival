
import numpy as np
import pandas as pd
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from gensim import corpora, models, similarities, matutils
import logging

from get_docs import *

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



def get_cv(docs, ngrams=(1,1), min_df=2, max_df=0.4):
    cv = CountVectorizer(ngram_range=ngrams, min_df=min_df, max_df=max_df)
    cv.fit(docs)
    return cv

def transform_with_cv(cv:CountVectorizer, docs):
    return cv.transform(docs).transpose()




def get_corpus(doc_word):
    return matutils.Sparse2Corpus(doc_word)

def get_id2word(cv):
    return dict((v, k) for k, v in cv.vocabulary_.items())


def perform_lda(corpus, id2word, num_topics, passes, workers):
    return models.LdaMulticore(corpus=corpus, id2word=id2word, num_topics=num_topics,
        passes=passes, workers=workers)



def lda_pipeline(num_topics, passes, workers, months=MONTHS, field='text', ngrams=(1,1), min_df=2, max_df=0.4):
    docs = get_docs(months, field=field)
    cv = get_cv(docs, ngrams=ngrams, min_df=min_df, max_df=max_df)
    doc_word = transform_with_cv(cv, docs)
    corpus = get_corpus(doc_word)
    id2word = get_id2word(cv)
    lda = perform_lda(corpus=corpus, id2word=id2word, num_topics=num_topics, passes=passes, workers=workers)
    return (cv, lda)
