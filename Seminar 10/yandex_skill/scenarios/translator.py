import nltk
import numpy as np
from nltk import word_tokenize
from gensim.models import KeyedVectors
from dialogic.cascade import DialogTurn

nltk.download('punkt')

uk_emb = KeyedVectors.load_word2vec_format("data/cc.uk.300.vec")
ru_emb = KeyedVectors.load_word2vec_format("data/cc.ru.300.vec")

with open('data/W.npy', 'rb') as f:
    W = np.load(f)


def translate(sentence):
    result = []
    for word in word_tokenize(sentence, language="russian"):
        if word in uk_emb.key_to_index:
            predicted = ru_emb.most_similar([np.matmul(uk_emb[word], W)])[0][0]
            result.append(predicted)
        else:
            result.append(word)
    return ' '.join(result)


def make_translation_response(turn: DialogTurn):
    text = turn.text
    if not text:
        return

    translation = translate(text)
    turn.response_text = f'Ваш перевод: "{translation}"'
