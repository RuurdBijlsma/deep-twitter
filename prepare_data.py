from gensim.models import Word2Vec, KeyedVectors
import sentencepiece
from os import cpu_count, replace
from variables import tweet_limit, use_nltk, sos, eos

if use_nltk:
    import nltk
    from nltk.tokenize import word_tokenize

    nltk.download('punkt')

model_name = "data/tweets.wv"
tweets_file = "data/tweets.txt"


def export_tweets_to_file(cursor):
    cursor.execute(f"SELECT cleaned from tweets LIMIT {tweet_limit}")
    with open(tweets_file, "w+", encoding="utf-8") as f:
        for [tweet] in cursor:
            f.write(tweet + "\n")


def get_max_sentence_length(cursor):
    max_sentence_length = 0
    for tokens in get_tokens(cursor):
        length = len(tokens)
        if length > max_sentence_length:
            max_sentence_length = length
    return max_sentence_length


sp = sentencepiece.SentencePieceProcessor()
tokenizer_model_file = "data/tokenizer.model"


def train_tokenizer():
    print("Training tokenizer now")
    sentencepiece.SentencePieceTrainer.Train(f'--input={tweets_file} --model_prefix=m --vocab_size=10000')
    replace("m.model", tokenizer_model_file)
    replace("m.vocab", "data/tokenizer.vocab")
    print("Training tokenizer complete")


def get_tokens(cursor):
    cursor.execute(f"SELECT cleaned from tweets LIMIT {tweet_limit}")
    for [tweet] in cursor:
        if use_nltk:
            tokens = [sos] + word_tokenize(tweet) + [eos]
        else:
            tokens = [sos] + sp.encode_as_pieces(tweet) + [eos]
        yield tokens

3
def get_w2v_model(cursor, retrain_w2v=False, retrain_tokenizer=False):
    if not use_nltk:
        if retrain_tokenizer:
            train_tokenizer()
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
