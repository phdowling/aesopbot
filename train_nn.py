import keras
from keras.models import Model
from keras.layers import LSTM, Input
from keras.preprocessing.sequence import pad_sequences

class Aesop(object):
    def __init__(self):
        self.model = None

    def build_model(self):
        chars_in = Input()