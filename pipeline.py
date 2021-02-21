from sklearn.base import BaseEstimator, TransformerMixin
from nlp import Nlp 

class TextPreProcessing(BaseEstimator, TransformerMixin):
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        nlp = Nlp()
        X = [nlp.remove_diacritics(doc) for doc in X]
        X = [nlp.remove_punctuations(doc) for doc in X]
        X = [nlp.normalize_arabic(doc) for doc in X]
        X = [nlp.num_to_text(doc) for doc in X]
        return X


class NlpPipeline(BaseEstimator, TransformerMixin):
    
    def __init__(self, lemmatization=True):
        self.lemmatization = lemmatization
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        nlp = Nlp()
        # Tokenization
        word_tokens = nlp.tokenize_doc(X)
        
        if( not self.lemmatization):
            # Stemming
            word_tokens = [nlp.stemmimg_text(w) for w in word_tokens]
        else:
            # Lemmatization
            word_tokens = [nlp.lemmatization_text(w) for w in word_tokens]

        # Stop words removal
        word_tokens = [nlp.remove_stop_words(w) for w in word_tokens]

        word_df = [' '.join([str(elem) for elem in doc]) for doc in word_tokens]
        
        return word_df