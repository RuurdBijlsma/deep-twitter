from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec, KeyedVectors
from variables import twitter_user
from nltk.tokenize import word_tokenize
import nltk
from os import cpu_count

nltk.download('punkt')
model_name = "data/tweets.wv"


def get_max_sentence_length(cursor):
    max_sentence_length = 0
    for tokens in get_tokens(cursor):
        length = len(tokens)
        if length > max_sentence_length:
            max_sentence_length = length
    return max_sentence_length


def get_tokens(cursor):
    cursor.execute("SELECT text from tweets")
    for [row] in cursor:
        yield word_tokenize(row)


def get_w2v_model(cursor, train=False):
    # Todo use the database text here

    if train:
        print("Building word2vec vocabulary")
        model = Word2Vec(size=100, window=5, min_count=1, iter=10, workers=cpu_count())
        model.build_vocab(get_tokens(cursor))
        print("Training word2vec model")
        model.train(get_tokens(cursor), total_examples=model.corpus_count, epochs=model.epochs)

        model.wv.save(model_name)
        model.save(model_name + '.model')
        print("Word2vec model saved to file")

        max_sentence_length = get_max_sentence_length(cursor)
        cursor.execute('INSERT INTO metadata VALUES(?,?)', (None, max_sentence_length))

    else:
        print("Skip training new word2vec model")

    wv = KeyedVectors.load(model_name, mmap='r')
    return wv
