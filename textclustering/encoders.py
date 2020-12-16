from sentence_transformers import SentenceTransformer
import numpy as np

class BertEncoder():
    ''' Class containing diferent sentence encoder options '''
    def __init__(self, batchSize: int=8, version: str='distilbert-base-nli-stsb-mean-tokens'):
        self.bertEncoder = SentenceTransformer(version)
        self.batchSize = batchSize

    def set_transformer_version(self, version: str):
        ''' Changes the transformer version used for encoding.
        Version options:
        'distilbert-base-nli-stsb-mean-tokens'
        'bert-large-nli-stsb-mean-tokens'
        'bert-large-nli-mean-tokens' '''

        self.bertEncoder = SentenceTransformer(version)

    def bert_encode(self, sentences: list):
        ''' Encodes the list of sentences with BERT encoder.
        Returns the list of vectors '''

        return np.stack(self.bertEncoder.encode(sentences,
                                                self.batchSize,
                                                show_progress_bar=True), axis=0)
