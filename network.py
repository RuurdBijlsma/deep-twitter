import numpy as np

from keras.callbacks import LambdaCallback
from keras.layers.recurrent import LSTM
from keras.layers.embeddings import Embedding
from keras.layers import Dense, Activation
from keras.models import Sequential
import keras
from prepare_data import get_tokens, sp

model_select = 'LSTM' 

def pre_train_model(cursor, word_model):
    checkpoint_path = "data/cp.ckpt"

    cursor.execute("SELECT count(cleaned) from tweets")
    (tweet_count,) = cursor.fetchone()
    cursor.execute("""
                    SELECT max_sentence_length
                    FROM metadata
                    WHERE id = (SELECT MAX(id) FROM metadata)
                    """)
    (max_sentence_len,) = cursor.fetchone()

    pretrained_weights = word_model.wv.vectors
    vocab_size, emdedding_size = pretrained_weights.shape
    print('Result embedding shape:', pretrained_weights.shape)

    # print('Checking similar words:')
    # for word in ['model', 'network', 'train', 'learn']:
    #     most_similar = ', '.join(
    #         '%s (%.2f)' % (similar, dist) for similar, dist in word_model.wv.most_similar(word)[:8])
    #     print('  %s -> %s' % (word, most_similar))

    def word2idx(word):
        return word_model.wv.vocab[word].index

    def idx2word(idx):
        return word_model.wv.index2word[idx]

    print('\nPreparing the data for LSTM...')
    train_x = np.zeros([tweet_count, max_sentence_len], dtype=np.int32)
    train_y = np.zeros([tweet_count], dtype=np.int32)
    for i, sentence in enumerate(get_tokens(cursor)):
        for t, word in enumerate(sentence[:-1]):
            train_x[i, t] = word2idx(word)
        train_y[i] = word2idx(sentence[-1])
    print('train_x shape:', train_x.shape)
    print('train_y shape:', train_y.shape)

    
    if model_select == 'LSTM':
        print('\nTraining LSTM...')
        model = Sequential()
        model.add(Embedding(input_dim=vocab_size, output_dim=emdedding_size, weights=[pretrained_weights]))
        model.add(LSTM(units=emdedding_size))
        model.add(Dense(units=vocab_size))
        model.add(Activation('softmax'))
        model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')
    if model_select == 'GAN': 
        model = gan

    def sample(preds, temperature=1.0):
        if temperature <= 0:
            return np.argmax(preds)
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)

    def generate_next(text, num_generated=10):
        word_idxs = [word2idx(word) for word in text.lower().split()]
        for i in range(num_generated):
            prediction = model.predict(x=np.array(word_idxs))
            idx = sample(prediction[-1], temperature=0.7)
            word_idxs.append(idx)
        return sp.decode_pieces(list(map(lambda idx: idx2word(idx), word_idxs)))

    def on_epoch_end(epoch, _):
        print('\nGenerating text after epoch: %d' % epoch)
        # TODO: Change prediction start thing from 55 yearrrrrs to styart of sentence token
        texts = [
            '<s>',
            '<s>',
            '<s>',
        ]
        for text in texts:
            sample = generate_next(text)
            print('%s... -> %s' % (text, sample))

    # Create a callback that saves the model's weights
    cp_callback = keras.callbacks.ModelCheckpoint(filepath=checkpoint_path,
                                                  save_weights_only=True,
                                                  verbose=1)

    model.summary()
    model.fit(train_x, train_y,
              batch_size=128,
              epochs=20,
              callbacks=[cp_callback, LambdaCallback(on_epoch_end=on_epoch_end)])

    return model
