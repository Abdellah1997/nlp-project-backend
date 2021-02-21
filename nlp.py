import pandas as pd
import re
import string
from num2words import num2words
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.isri import ISRIStemmer
import qalsadi.lemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

class Nlp:
    
    def __init__(self):
        self.arabic_diacritics = re.compile("""
                                ّ    | # Tashdid
                                َ    | # Fatha
                                ً    | # Tanwin Fath
                                ُ    | # Damma
                                ٌ    | # Tanwin Damm
                                ِ    | # Kasra
                                ٍ    | # Tanwin Kasr
                                ْ    | # Sukun
                                ـ     # Tatwil/Kashida
                            """, re.VERBOSE)

        self.arabic_punctuations = '''`÷×؛<>_()*&^%][ـ،/:"؟.,'{}~¦+|!”…“–ـ'''
        self.english_punctuations = string.punctuation
        self.punctuations_list = self.arabic_punctuations + self.english_punctuations

    def remove_diacritics(self, text):
        text = re.sub(self.arabic_diacritics, '', text)
        return text

    def remove_punctuations(self, text):
        translator = str.maketrans('', '', self.punctuations_list)
        return text.translate(translator)

    def normalize_arabic(self, text):
        text = re.sub("[إأآا]", "ا", text)
        text = re.sub("ؤ", "ء", text)
        text = re.sub("ئ", "ء", text)
        text = re.sub("گ", "ك", text)
        return text

    def num_to_text(self, text):
        out = ''
        for s in text.split():
            if s.isdigit():
                out = out + num2words(int(s), lang='ar')+' '
            else:
                out = out+ s +' '
        return out[:-1]

    def tokenize_doc(self, doc):
        return [word_tokenize(text) for text in doc]

    def remove_stop_words(self, text):
        f = open('list.txt', 'r',encoding="utf8")
        stopword = f.read().splitlines()+ stopwords.words("arabic")
        return [w for w in text if w not in stopword]
    
    def stemmimg_text(self, text):
        st = ISRIStemmer()
        return[st.stem(w) for w in text]
    
    def lemmatization_text(self, text):
        lemmer = qalsadi.lemmatizer.Lemmatizer()
        return [lemmer.lemmatize(w) for w in text]
    
    def tfdif_doc(self, doc):   
        vectorizer = TfidfVectorizer()
        return vectorizer.fit_transform(doc)
