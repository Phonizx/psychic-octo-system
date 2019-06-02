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


pred = predictor("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
cleaning = TextPreparation('')
documenti = pred.get_documents()


@app.route("/") #da sistemare
def home():
    cleaning.load_stopWord("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/stop_words.txt") #paths
    pred.restore_model("/home/phinkie/Scrivania/tes/psychic-octo-system/Models/0601 080/model.tflearn",554,240)

    return  "Model: ok"
    '''
    path = "C:\\Nuova cartella\\psychic-octo-system\\"
    pred = predictor(path+"dataUtils\\")#("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
#"/home/phinkie/Scrivania/psychic-octo-system/
    model = pred.restore_model(path+"Models\\0601 080\\model.tflearn",554,240)
    return "Model caricato !"
    '''


@app.route("/getDocuments/<richiesta>",methods=['GET'])
def getDocuments(richiesta):
    domanda = cleaning.prepare_sentence(richiesta)
    processed = " ".join(domanda)
    id_docs = pred.prediction(processed) # 3 documenti piu probabili
    return json.dumps(id_docs)

@app.route("/Domanda",methods=['GET'])
def domanda():
    domanda = request.args.get('richiesta')
    docs = getDocuments(domanda)
    resp = documenti[int(docs[0])]["documento"]
    return render_template('index.html', context=resp + str(docs))

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
