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
path = "C:\\Nuova cartella\\psychic-octo-system\\"
#/home/phinkie/Scrivania/psychic-octo-system
pred = predictor(path+"dataUtils\\")
cleaning = TextPreparation("C:\\Nuova cartella\\psychic-octo-system\\")
documenti = pred.get_documents()


@app.route("/") #da sistemare
def home():
    #"/home/phinkie/Scrivania/psychic-octo-system/
    cleaning.load_stopWord(path+"dataUtils\\stop_words.txt") #paths
    #"/home/phinkie/Scrivania/tes/psychic-octo-system/
    pred.restore_model(path+"Models\\0601 080\\model.tflearn",554,240)

    return  "Model: ok"
    '''
    pred = predictor(path+"dataUtils\\")#("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
    #"/home/phinkie/Scrivania/psychic-octo-system/
    model = pred.restore_model(path+"Models\\0601 080\\model.tflearn",554,240)
    return "Model caricato !"
    '''


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
