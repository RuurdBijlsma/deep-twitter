from gensim.test.utils import common_texts, get_tmpfile
from gensim.models import Word2Vec, KeyedVectors
from variables import twitter_user
from nltk.tokenize import word_tokenize
import sentencepiece
# import nltk
from os import cpu_count, replace

# nltk.download('punkt')
model_name = "data/tweets.wv"


def get_max_sentence_length(cursor):
    max_sentence_length = 0
    for tokens in get_tokens(cursor):
        length = len(tokens)
        if length > max_sentence_length:
            max_sentence_length = length
    return max_sentence_length


sp = sentencepiece.SentencePieceProcessor()
tokenizer_model_file = "data/tokenizer.model"


def train_tokenizer(cursor):
    cursor.execute("SELECT text from tweets")
    vocab_file = "data/tweets.txt"
    with open(vocab_file, "w+", encoding="utf-8") as f:
        for [text] in cursor:
            f.write(text + "\n")

    print("Training tokenizer now")
    sentencepiece.SentencePieceTrainer.Train(f'--input={vocab_file} --model_prefix=m --vocab_size=10000')
    replace("m.model", tokenizer_model_file)
    replace("m.vocab", "data/tokenizer.vocab")
    print("Training tokenizer complete")


def get_tokens(cursor):
    cursor.execute("SELECT text from tweets")
    for [row] in cursor:
        tokens = sp.encode_as_pieces(row)
        yield tokens


def get_w2v_model(cursor, retrain_w2v=False, retrain_tokenizer=False):
    # Todo use the database text here
    if retrain_tokenizer:
        train_tokenizer(cursor)
    sp.load(tokenizer_model_file)

    if retrain_w2v:
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
