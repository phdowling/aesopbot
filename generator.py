import keras
from keras.models import load_model
import random
import numpy as np
import sys
import requests

URL = "http://localhost:80/new_lyrics"


print "read data.."
text = open("all_lyrics_kanye.txt").read().lower()

print 'corpus length:', len(text)


text = text[:600000]

model = load_model("trained_kanye.model")
# model.load_weights("trained_kanye.model.weights")

print('corpus length:', len(text))

chars = sorted(list(set(text)))
chars += ["X"] * (143 - len(chars))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

# cut the text in semi-redundant sequences of maxlen characters
maxlen = 40
step = 3
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1
    y[i, char_indices[next_chars[i]]] = 1


def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


def generate_bars():
    start_index = random.randint(0, len(text) - maxlen - 1)
    for diversity in [0.8, 1.0, 1.1, 1.4]:
        print
        print '----- diversity:', diversity
        generated = ''
        sentence = text[start_index: start_index + maxlen]
        yield sentence, "SEED"
        generated += sentence
        print '----- Generating with seed: "' + sentence + '"'
        sys.stdout.write(generated)
        for i in range(400):
            x = np.zeros((1, maxlen, len(chars)))
            for t, char in enumerate(sentence):
                x[0, t, char_indices[char]] = 1.
            preds = model.predict(x, verbose=0)[0]
            next_index = sample(preds, diversity)
            next_char = indices_char[next_index]
            generated += next_char
            sentence = sentence[1:] + next_char

            sys.stdout.write(next_char)
            sys.stdout.flush()

            yield next_char, "GEN"
        print


def run():
    while True:
        print "seeding.."
        for seq, source in generate_bars():
            print "sending %s (%s)" % (seq, source)
            res = requests.post(URL, json={"lyrics": seq, "isGenerated": source == "GEN"})


if __name__ == "__main__":
    run()
