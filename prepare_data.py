from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec, KeyedVectors

model_name = "tweets.wv"


def prepare_data(cursor, train=True):
    # Todo use the database text here
    if train:
        model = Word2Vec(common_texts, size=100, window=5, min_count=1, workers=4)
        model.wv.save(model_name)
        model.save(model_name + '.model')

    wv = KeyedVectors.load(model_name, mmap='r')
    computer_vec = wv['computer']

    return 1, 2