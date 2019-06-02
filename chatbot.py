import os
import json
import numpy as np

from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template

from pymongo import MongoClient

from octosystem import predictor
from Utils import TextPreparation
from flask import jsonify


app = Flask(__name__)
# TODO: utilizzare path relativo
#pred = predictor("C:\\Nuova cartella\\psychic-octo-system\\dataUtils\\")
#cleaning = TextPreparation("C:\\Nuova cartella\\psychic-octo-system\\")

pred = predictor("/home/phinkie/Scrivania/tes/psychic-octo-system/dataUtils/")
cleaning = TextPreparation("/home/phinkie/Scrivania/tes/psychic-octo-system/")

documenti = pred.get_documents()


@app.route("/") #da sistemare
def home():

    #cleaning.load_stopWord("C:\\Nuova cartella\\psychic-octo-system\\dataUtils\\stop_words.txt") #paths
    #pred.restore_model("C:\\Nuova cartella\\psychic-octo-system\\Models\\0601 080\\model.tflearn",554,240)

    pred.restore_model("/home/phinkie/Scrivania/tes/psychic-octo-system/Models/0601 080/model.tflearn",554,240)
    cleaning.load_stopWord("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/stop_words.txt")

    return render_template('index.html', context="") #"Model: ok"


@app.route("/getDocuments/<richiesta>", methods=['GET'])
def getDocuments(richiesta):
    domanda = cleaning.prepare_sentence(richiesta)
    processed = " ".join(domanda)
    id_docs = pred.prediction(processed) # 3 documenti piu probabili
    docs =  [documenti[i] for i in id_docs]
    tmp = json.dumps(docs, indent=4)
    return tmp


@app.route("/domanda", methods=['GET'])
def domanda():
    domanda = request.args.get('richiesta')
    docus = getDocuments(domanda) #[doc0, doc1, doc2]
    docs = json.loads(docus)
    #resp = docs[0]["documento"]
    contenuto = "".join([d["documento"]+"\n" for d in docs])
    return render_template('index.html', context=contenuto)

@app.route("/servizio", methods=['GET'])
def servizio():
    domanda = request.args.get('richiesta')
    docus = getDocuments(domanda) #[doc0, doc1, doc2]
    docs = json.loads(docus)
    contenuto = "".join([d["servizio"]+"\n" for d in docs])
    return render_template('index.html', context=contenuto)

@app.route("/allegati", methods=['GET'])
def allegati():
    domanda = request.args.get('richiesta')
    docus = getDocuments(domanda) #[doc0, doc1, doc2]
    docs = json.loads(docus)
    links = [d["allegati"] for d in docs]
    contenuto = "".join([str(link)+"\n\n\n\n\n" for link in links])
    return render_template('index.html', context=contenuto)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
