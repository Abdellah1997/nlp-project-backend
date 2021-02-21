import pickle
from flask import Flask, request, Response
import json
from pipeline import TextPreProcessing, NlpPipeline
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from flask_cors import CORS


model_sentiment = pickle.load(open('models/sentimentSVC.pkl', 'rb'))
model_fakeNews = pickle.load(open('models/fakeNewsSVC.pkl', 'rb'))

app = Flask(__name__)

CORS(app)

@app.route('/sentiment', methods=['post'])
def predict_sentiment():
    # nltk.download('punkt')
    # nltk.download('stopwords')
    request_data = request.get_json()
    text = request_data['text']
    print(text)
    prediction = model_sentiment.predict([text])
    print(prediction)
    return Response(response=prediction[0],status = 200,mimetype="application/json")

@app.route('/fakeNews', methods=['post'])
def predict_fakeNews():
    # nltk.download('punkt')
    # nltk.download('stopwords')
    request_data = request.get_json()
    text = request_data['text']
    print(text)
    prediction = model_fakeNews.predict([text])
    print(prediction)
    return Response(response=prediction[0],status = 200,mimetype="application/json")

@app.route('/nlp', methods=['post'])
def nlp():
    request_data = request.get_json()
    docs = request_data['docs']

    nlp = Pipeline([
    ('pre-processing', TextPreProcessing()),
    ('nlp', NlpPipeline())
    #('TF-IDF',TfidfVectorizer()),
    ])
    docs_nlp = nlp.fit_transform([docs]) # .toarray()

    return Response(response=json.dumps(docs_nlp[0]),status = 200,mimetype="application/json") #docs_nlp.toList()

if __name__ == '__main__':
   app.run(debug = True)