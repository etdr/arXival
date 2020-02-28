
import numpy as np
import pandas as pd

from gensim.models import FastText
from gensim.utils import tokenize, RULE_DEFAULT, RULE_DISCARD, RULE_KEEP
from pymongo import MongoClient
import logging

from string import ascii_letters, ascii_lowercase, ascii_uppercase
from get_docs import *
from wordlist import words

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


ascii_upper_plus = ascii_uppercase + '.'




def get_docs_split_gen(docs):
    def gen():
        i = 0
        while i < len(docs):
            yield docs[i].split()
            i += 1
            
    return gen



# https://jacopofarina.eu/posts/gensim-generator-is-not-iterator/
class DocIterator():
    def __init__(self, gen_function):
        self.gen_function = gen_function
        self.generator = self.gen_function()
    def __iter__(self):
        self.generator = self.gen_function()
        return self
    def __next__(self):
        result = next(self.generator)
        if result is None:
            raise StopIteration
        else:
            return result
    


def get_fasttext_model(docs_split_gen, size=20, window=3, min_count=16, workers=5, sg=0):
    model = FastText(size=size, window=window, min_count=min_count, trim_rule=trim_rule,
        workers=workers, sg=sg)
    model.build_vocab(sentences=docs_split_gen)
    return model

def train_model(model, docs_split_gen, len_docs, epochs=10):
    model.train(sentences=docs_split_gen, total_examples=len_docs, epochs=epochs)



# this is very similar to the validate_word functions from process_docs
def trim_rule(w, c, min_count):
    print(w)
    if c >= min_count: return RULE_KEEP
    if w in words: return RULE_KEEP
    if w[0].lower()+w[1:] in words: return RULE_KEEP
    if all(c in ascii_upper_plus for c in w) and w.lower() in words: return RULE_KEEP
    if all(subw in words for subw in w.split('-')): return RULE_KEEP
    return RULE_DISCARD


def get_vector_df(model):
    return pd.DataFrame({w: model.wv.word_vec(w) for w in model.wv.vocab.keys()}).transpose()
