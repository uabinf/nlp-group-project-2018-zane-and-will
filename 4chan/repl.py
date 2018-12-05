#!/usr/bin/env python3
import os
import gensim
import readline
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

nltk.download('stopwords')

class Model:
    def __init__(self, board):
        self.board = 'news'
        self.stemmer = LancasterStemmer()
        self.load(board)

    def build(self):
        self.stem_map = dict()
        print(f'building /{self.board}/ model')
        stop_words = set(stopwords.words('english'))
        with open(f'text/{self.board}/comments', 'r') as f:
            posts = []
            for post in f.readlines():
                tokens = []
                for word in post.split():
                    if word not in stop_words:
                        stemmed_word = self.stemmer.stem(word)
                        if stemmed_word in self.stem_map.keys():
                            self.stem_map[stemmed_word].add(word)
                        else:
                            self.stem_map[stemmed_word] = set([word])
                        tokens.append(stemmed_word)
                posts.append(tokens)
        self.model = gensim.models.Word2Vec(posts, workers=8, size=250)
        self.save()

    def save(self):
        self.model.save(f'models/{self.board}.model')
        with open(f'models/{self.board}.map', 'wb') as f:
            pickle.dump(self.stem_map, f)

    def load(self, board, force=False):
        self.board = board
        #self.grams = []
        print(f'loading /{self.board}/ model')
        if force:
            self.build()
            return
        try:
            self.model = gensim.models.Word2Vec.load(f'models/{self.board}.model')
            with open(f'models/{self.board}.map', 'rb') as f:
                self.stem_map = pickle.load(f)
        except FileNotFoundError:
            self.build()

    def find(self, user_input):
        try:
            split = user_input.split(' ')
            word = split[0]
            num = int(split[1])
        except IndexError:
            word = user_input
            num = 10
        try:
            print(self.model.wv.most_similar(self.stemmer.stem(word), topn=num))
        except KeyError:
            print(f"{word} is not in the vocabulary")

    def compare(self, w1, w2):
        w1 = self.stemmer.stem(split[1])
        w2 = self.stemmer.stem(split[2])
        print(model.wv.similarity(w1, w2))

    def expand(self, word):
        try:
            to_print = self.stem_map[word]
        except KeyError:
            to_print = f'Stem {word} not found in this model.'
        print(to_print)

'''
    def five_grams(self, word):
        with open(f'text/{self.board}/comments', 'r') as f:
            for line in f.readlines():
                self.grams += nltk.ngrams(line.split(), 5)
        hits = {}
        for gram in self.grams:
            if word in gram:
                if gram in hits:
                    hits[gram] += 1
                else:
                    hits[gram] = 1
        culled = [{i[0]:i[1]} for i in hits.items() if i[1] > 1]
        if len(culled) > 0:
            print(culled[:10])
        else:
            print("No non-unique ngrams to show.")
            print([hits])
'''

def repl():
    user_input = ''
    board = 'news'
    model = Model(board)
    while True:
        user_input = input("> ")
        if ':q' in user_input:
            return

        elif ':o!' in user_input:
            board = user_input.split(' ')[1]
            model.load(board, True)

        elif ':o' in user_input:
            board = user_input.split(' ')[1]
            model.load(board)

        elif ':compare' in user_input:
            split = user_input.split(' ')
            if len(split) < 3:
                print('Not enough args given.')
                continue
            w1 = split[1]
            w2 = split[2]
            model.compare(w1, w2)

        elif ':e' in user_input:
            split = user_input.split(' ')
            if len(split) < 2:
                print('No args given.')
                continue
            model.expand(split[1])

'''
        elif ':n' in user_input:
            split = user_input.split(' ')
            if len(split) < 2:
                print('No args given.')
                continue
            model.five_grams(split[1])
'''

        else:
            model.find(user_input)


if __name__ == '__main__':
    if not os.path.exists('models'):
        os.mkdir('models')
    repl()
