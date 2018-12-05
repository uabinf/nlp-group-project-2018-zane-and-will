import gensim

model = gensim.models.Word2Vec(sentences, workers=8, size=300, window=50, min_count=50)

