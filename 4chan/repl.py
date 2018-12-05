#!/usr/bin/env python3
import os
import gensim
import readline
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from nltk import download

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

download('stopwords')
stemmer = LancasterStemmer()

class Model:
    def __init__(board):

    def load(self, board, force=False):
        pass

    def build_model(self, board):
        print(f'loading /{board}/ model')
        if force:
            self.build_model(board)
            return
        try:
            self.model = gensim.models.Word2Vec.load(f'models/{board}.model')
        except FileNotFoundError:
            self.build_model(board)

def build_model(board):
    print(f'building /{board}/ model')
    stop_words = set(stopwords.words('english'))
    with open(f'text/{board}/comments', 'r') as f:
        posts = [[stemmer.stem(word) for word in post.split() \
                if word not in stop_words] \
                for post in f.readlines()]
    model = gensim.models.Word2Vec(posts, workers=8, size=250)
    model.save(f'models/{board}.model')
    return model

def load_model(board, force=False):
    print(f'loading /{board}/ model')
    if force:
        return build_model(board)
    try:
        return gensim.models.Word2Vec.load(f'models/{board}.model')
    except FileNotFoundError:
        return build_model(board)

def expand(model, word):
    pass

def repl():
    user_input = ''
    board = 'news'
    model = load_model(board)
    while True:
        user_input = input("> ")
        if ':q' in user_input:
            return
        elif ':o!' in user_input:
            board = user_input.split(' ')[1]
            model = load_model(board, True)
        elif ':o' in user_input:
            board = user_input.split(' ')[1]
            model = load_model(board)
        elif ':compare' in user_input:
            w1 = stemmer.stem(user_input.split(' ')[1])
            w2 = stemmer.stem(user_input.split(' ')[2])
            print(model.wv.similarity(w1, w2))
        else:
            try:
                print(model.wv.most_similar(stemmer.stem(user_input)))
            except KeyError:
                print(f">>> {user_input} is not in the vocabulary")

if __name__ == '__main__':
    if not os.path.exists('models'):
        os.mkdir('models')
    repl()
