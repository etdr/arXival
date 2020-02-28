
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
from pymongo import MongoClient
import re

from string import ascii_letters, ascii_lowercase, ascii_uppercase
import characters as chars

from get_docs import *
from wordlist import words

if tf.config.experimental.list_physical_devices('GPU'):
    tf.config.experimental.set_memory_growth(tf.config.experimental.list_physical_devices('GPU')[0], True)


WINDOW_SIZE = 2




# for i in range(len(docs)): 
#      ...:     doci_wds = docs[i].split() 
#      ...:     doci_f_wds = docs_filtered[i].split() 
#      ...:     nonwords = [] 
#      ...:     for w in doci_wds: 
#      ...:         if w not in doci_f_wds: 
#      ...:             nonwords.append(w) 
#      ...:     counter.update(nonwords) 
#      ...:     print(i) 















def get_dataset(docs):
    def yield_docs():
        i = 0
        while i < len(docs):
            yield docs[i]
            i += 1
    dataset = tf.data.Dataset.from_generator(yield_docs, output_types=tf.string, output_shapes=(),)
    return dataset


def get_vocab_set(dataset, num_words=100000):
    tokenizer = tfds.features.text.Tokenizer()
    #tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=num_words, filters='')
    vocab_set = set()
    i = 0
    for text_t in dataset:
        tokens = tokenizer.texts_to_sequences([text_t.numpy()])
        vocab_set.update(tokens)
        print('vocab size',len(vocab_set),'; finished document',i)
        i += 1
    return vocab_set

def get_vocab_encoder(vocab_set):
    return tfds.features.text.TokenTextEncoder(vocab_set)        


def get_keras_tokenizer(docs, num_words=100000, filters=''):
    tokenizer = tf.keras.preprocessing.text.Tokenizer(num_words=num_words, filters='')
    tokenizer.fit_on_texts(docs)
    return tokenizer

def get_vocab_set_v2(tokenizer, num_words=100000):
    vocab_set = set()
    for k, v in tokenizer.word_index.items():
        if v <= num_words - 1:
            vocab_set.add(k)
    return vocab_set

def get_docs_split(docs):
    return [d.split() for d in docs]

def filter_docs_using_tokenizer(docs_split, vocab_set):
    return [list(filter(lambda w: w in vocab_set, doc)) for doc in docs_split]




shifts = list(range(-WINDOW_SIZE, WINDOW_SIZE))
shifts.remove(0)

def get_training_generator(docs_split, encoder, window_size=WINDOW_SIZE, buffer_size=10000):
    dataset_shuffled = dataset.shuffle(buffer_size=buffer_size)
    lds = len(docs_split)
    def gen():
        while True:
            #doc = [d.numpy().split() for d in dataset_shuffled.take(1)][0]
            doc = docs_split[np.random.randint(0,lds)]
            target_index = np.random.randint(0, len(doc)-1)
            input_index = -1
            while input_index < 0 or input_index >= len(doc):
                shift = np.random.choice(shifts)
                input_index = target_index + shift
            target_vector = tf.one_hot(encoder.encode(doc[target_index]), encoder.vocab_size)
            input_vector = np.array([encoder.encode(doc[input_index])]) 
            print('input shape',input_vector.shape,' ; output shape',target_vector.shape)
            yield (input_vector, target_vector)
            
    return gen


def get_training_generator_v2(docs_split, tokenizer, n_samples=2000000, window_size=WINDOW_SIZE):
    lds = len(docs_split)
    num_words = tokenizer.num_words
    def gen():
        i = 0
        while i < n_samples:
            i += 1
            doc = docs_split[np.random.randint(0,lds)]
            target_index = np.random.randint(0, len(doc)-1)
            input_index = -1
            while input_index < 0 or input_index >= len(doc):
                shift = np.random.choice(shifts)
                input_index = target_index + shift
            target_vector = tf.one_hot(tokenizer.texts_to_sequences([doc[target_index]])[0], num_words)
            input_vector = np.array(tokenizer.texts_to_sequences([doc[input_index]]))
            yield (input_vector, target_vector)

    return gen




def build_nn(num_words, dimension, optimizer=tf.keras.optimizers.SGD(), loss=tf.keras.losses.CategoricalCrossentropy()):
    nn = tf.keras.models.Sequential()
    nn.add(tf.keras.layers.Embedding(num_words, dimension, input_length=1))
    nn.add(tf.keras.layers.Flatten())
    nn.add(tf.keras.layers.Dense(num_words, activation='softmax'))
    nn.compile(optimizer=optimizer, loss=loss)
    return nn


def train_nn(nn, g):
    return nn.fit(x=g)





from numpy import dot
from numpy.linalg import norm

def cossim(x, y):
    return dot(x, y) / (norm(x) * norm(y))


def t_encode(s, tokenizer):
    return tokenizer.texts_to_sequences([s])[0]

def t_encode_word(w, tokenizer):
    return tokenizer.texts_to_sequences([w])[0][0]



def get_similar_words(w, tokenizer, embeddings):
    pass











#from https://colab.research.google.com/github/tensorflow/docs/blob/master/site/en/tutorials/load_data/text.ipynb#scrollTo=K0BjCOpOh7Ch
def labeler(example, index):
    return example, tf.cast(index, tf.int64)
