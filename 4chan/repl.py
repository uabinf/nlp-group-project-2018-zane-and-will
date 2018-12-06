#!/usr/bin/env python3
import os
import gensim
import readline
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer
from operator import itemgetter

import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

nltk.download('stopwords')

class InsufficientArgs(Exception):
    def __init__(self, expected_num):
        print(f'not enough args given, expected {expected_num} args')

class Model:
    def __init__(self, board):
        self.board = 'news'
        self.stemmer = LancasterStemmer()
        self.load(board)

    def build(self):
        print(f'building /{self.board}/ model')
        stop_words = set(stopwords.words('english'))
        with open(f'text/{self.board}/comments', 'r') as f:
            for post in f.readlines():
                tokens = list()
                for word in post.split():
                    if word not in stop_words:
                        stemmed_word = self.stemmer.stem(word)
                        if stemmed_word in self.stem_map.keys():
                            self.stem_map[stemmed_word].add(word)
                        else:
                            self.stem_map[stemmed_word] = set([word])
                        tokens.append(stemmed_word)
                self.posts.append(tokens)
        self.model = gensim.models.Word2Vec(self.posts, workers=8, size=250)

    def save(self):
        print(f'saving {self.board}/ model')
        self.model.save(f'models/{self.board}.model')
        with open(f'models/{self.board}.dat', 'wb') as f:
            data = {'posts':self.posts,
                    'stem_map':self.stem_map,
                    'grams': self.grams}
            pickle.dump(data, f)

    def load(self, board, force=False):
        print(f'loading /{self.board}/ model')
        self.board = board
        self.posts = list()
        self.stem_map = dict()
        self.grams = dict()
        if force:
            self.build()
            return
        try:
            self.model = gensim.models.Word2Vec.load(f'models/{self.board}.model')
            with open(f'models/{self.board}.dat', 'rb') as f:
                data = pickle.load(f)
                self.stem_map = data['stem_map']
                self.posts = data['posts']
                self.grams = data['grams']
        except FileNotFoundError:
            self.build()

    def reload(self):
        self.load(self.board, True)

    def build_ngrams(self, lower_bound, upper_bound):
        lower_bound = int(lower_bound)
        upper_bound = int(upper_bound)
        self.grams = {i:[] for i in range(lower_bound, upper_bound+1)}
        for i in range(lower_bound, upper_bound+1):
            print(f'building {i}-grams')
            for post in self.posts:
                self.grams[i] += nltk.ngrams(post, i)

    def compare(self, w1, w2):
        w1 = self.stemmer.stem(split[1])
        w2 = self.stemmer.stem(split[2])
        print(model.wv.similarity(w1, w2))

    def expand(self, word):
        try:
            to_print = self.stem_map[word]
        except KeyError:
            to_print = f'stem {word} not found in this model'
        print(to_print)

    def ngrams(self, n, count=10):
        hits = {}
        n = int(n)
        count = int(count)
        if n not in self.grams.keys():
            print(f'{n}-grams not built')
            print(f'{self.grams.keys()} have been built')
            return
        for gram in self.grams[n]:
                if gram in hits:
                    hits[gram] += 1
                else:
                    hits[gram] = 1
        culled = [(i[0], i[1]) for i in hits.items() if i[1] > 1]
        culled = sorted(culled, key=itemgetter(1))
        culled.reverse()
        if len(culled) > 0:
            print(culled[:count])
        else:
            print("no non-unique ngrams to show")

    def find(self, word, n=10):
        try:
            print(self.model.wv.most_similar(self.stemmer.stem(word), topn=n))
        except KeyError:
            print(f"{word} is not in the vocabulary")


def extract_args(user_input, expected_num):
    if not isinstance(expected_num, list):
        expected_num = [expected_num]
    split = user_input.split(' ')
    if len(split) - 1 not in expected_num:
        raise InsufficientArgs(expected_num)
    return split[1:]

def repl():
    user_input = ''
    board = 'news'
    model = Model(board)
    while True:
        user_input = input("> ")
        try:
            if ':q' in user_input:
                return

            elif ':?' in user_input:
                print(':q           -- quit.')
                print(':o board     -- load a board model, building it if not found.')
                print(':o! board    -- load a board model, building it.')
                print(':w           -- save a board model.')
                print(':[bm/r]      -- rebuilds the current model.')
                print(':bn i j      -- builds i-grams through j-grams.')
                print(':c w1, w2    -- compares the similarity of w1 and w2.')
                print(':e stem      -- shows all words that reduce to that stem.')
                print(':n n [x]     -- shows the top x n-grams.')
                print('<word> [x]   -- shows the top x most similar words to word.')

            elif ':o!' in user_input:
                board = extract_args(user_input, 1)
                model.load(*board, True)

            elif ':o' in user_input:
                board = extract_args(user_input, 1)
                model.load(*board)

            elif ':w' in user_input:
                model.save()

            elif ':bm' in user_input or ':r' in user_input:
                model.reload()

            elif ':bn' in user_input:
                lower, upper = extract_args(user_input, 2)
                model.build_ngrams(lower, upper)

            elif ':c' in user_input:
                w1, w2 = extract_args(user_input, 2)
                model.compare(w1, w2)

            elif ':e' in user_input:
                word = extract_args(user_input, 1)
                model.expand(*word)

            elif ':n' in user_input:
                args = extract_args(user_input, [1, 2])
                model.ngrams(*args)

            else:
                args = extract_args(user_input, [0, 1])
                model.find(*args)

        except InsufficientArgs:
            continue


if __name__ == '__main__':
    if not os.path.exists('models'):
        os.mkdir('models')
    repl()
