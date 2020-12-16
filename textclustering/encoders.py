from sentence_transformers import SentenceTransformer
# import tensorflow_hub as hub
from src.config import Config
import numpy as np

config = Config()

class Encoders():
    '''
    Class containing diferent sentence encoder options.
    '''
    def __init__(self, batchSize=8):
        self.bertEncoder = SentenceTransformer(config.bertVersionDefault)
        self.batchSize = batchSize

    def setTransformerVersion(self, version):
        '''
        Changes the transformer version used for encoding.
        Version options:
        'distilbert-base-nli-stsb-mean-tokens'
        'bert-large-nli-stsb-mean-tokens'
        'bert-large-nli-mean-tokens'
        '''

        self.bertEncoder = SentenceTransformer(version)

    def bert_encode(self, sentences):
        '''
        Encodes the list of sentences with BERT encoder.
        Returns the list of vectors.
        '''

        return np.stack(self.bertEncoder.encode(sentences,
                                                self.batchSize,
                                                show_progress_bar=True), axis=0)
