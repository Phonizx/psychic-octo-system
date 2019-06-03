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

#SigSky
#pred = predictor("C:\\Nuova cartella\\psychic-octo-system\\dataUtils\\")
#cleaning = TextPreparation("C:\\Nuova cartella\\psychic-octo-system\\")

#phonix
pred = predictor("/home/phinkie/Scrivania/tes/psychic-octo-system/dataUtils/")
cleaning = TextPreparation("/home/phinkie/Scrivania/tes/psychic-octo-system/")

documenti = None


@app.route("/") #da sistemare
def home():



    return render_template('index.html', context="") #"Model: ok"


@app.route("/getDocuments/<richiesta>", methods=['GET']) #da sistemare
def getDocuments(richiesta):
    domanda = cleaning.prepare_sentence(richiesta)
    processed = " ".join(domanda)
    resp = [] #json objects

    id_docs = pred.prediction(processed) # 3 documenti piu probabili

    documents = documenti[id_docs[0]]
    resp.append(documents)
    ids = [int(item) for item in id_docs]
    resp.append(ids)

    tmp = json.dumps(resp, indent=4)
    return tmp


@app.route("/domanda", methods=['GET'])
def domanda():
    domanda = request.args.get('richiesta')
    docus = getDocuments(domanda) #[doc0, doc1, doc2]
    docs = json.loads(docus)
    contenuto = docs[0]
    #resp = docs[0]["documento"]
    #contenuto = "".join([d["documento"]+"\n" for d in docs])
    return render_template('index.html', context=contenuto["documento"])

@app.route("/servizio", methods=['GET'])
def servizio():
    id = request.args.get('id_doc')
    contenuto = documenti[int(id)]["servizio"]
    return render_template('index.html', context=contenuto)

@app.route("/allegati", methods=['GET'])
def allegati():
    id = request.args.get('id_doc')
    contenuto = documenti[int(id)]["allegati"]
    contenuto = "".join([str(link)+"\n\n\n\n\n" for link in contenuto])
    return render_template('index.html', context=contenuto)

if __name__ == "__main__":
    #SigSky
    #cleaning.load_stopWord("C:\\Nuova cartella\\psychic-octo-system\\dataUtils\\stop_words.txt") #paths
    #pred.restore_model("C:\\Nuova cartella\\psychic-octo-system\\Models\\0601 080\\model.tflearn",554,240)

    #phonix
    pred.restore_model("/home/phinkie/Scrivania/tes/psychic-octo-system/Models/0601 080/model.tflearn",554,240)
    cleaning.load_stopWord("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/stop_words.txt")
    documenti = pred.get_documents()
    app.run(host='0.0.0.0',debug=True)
