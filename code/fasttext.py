
from gensim.models import FastText
from gensim.utils import tokenize
from pymongo import MongoClient


client = MongoClient()
db = client.arXiv
c1901 = db['1901']


def get_docs_as_list(month):
    c = db[month]



def get_fasttext_model(docs, size=20, window=3, min_count=20):
    model = FastText(size=size, window=window, min_count=min_count)
    model.build_vocab(sentences=docs)
    return model

def train_model(model, docs, epochs=10):
    model.train(sentences=docs, total_examples=len(docs), epochs=epochs)


