import os
import json
import numpy as np

from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template

from pymongo import MongoClient


from flask import jsonify

#from .octosystem import predictor
#from .Utils import TextPreparation

app = Flask(__name__,template_folder='templates')


#pred = predictor("/app/dataUtils/")
#cleaning = TextPreparation("/app/")

documenti = None
store_ids = [0,0,0] #conserva gli id dei documenti correnti

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

@app.route("/getDoc/<id>", methods=['GET'])
def getDoc(id):
    id = int(id)
    if (id < 0):
        id = 0
    return json.dumps(documenti[id])

@app.route("/mostraDoc/<id>", methods=['GET'])
def mostraDoc(id):
    id = int(id)
    if (id < 0):
        id = 0
    doc = documenti[id]["documento"]
    return render_template('index.html', context=doc,id0=id)

@app.route("/mostraTitoli/<id1>/<id2>", methods=['GET'])
def mostraTitoli(id1, id2):
    id1_ = int(id1)
    id2_ = int(id2)
    doc1 = json.loads(getDoc(id1_))
    doc2 = json.loads(getDoc(id2_))

    tit1 = doc1["documento"].split('Cosa')[0]
    tit2 = doc2["documento"].split('Cosa')[0]
    return render_template('index.html', id1=id1_, id2=id2_, titolo1=tit1, titolo2=tit2)



@app.route("/domanda", methods=['GET'])
def domanda():
    domanda = request.args.get('richiesta')
    if(isNotRequest(domanda) and len(store_ids) > 0):
        return redirect(url_for("mostraTitoli",id1=store_ids[1],id2=store_ids[2]))
    else:
        docus = getDocuments(domanda) #[doc0, doc1, doc2]
        docs = json.loads(docus)
        contenuto = docs[0]

        for i in range(0,len(docs[1])):
            store_ids[i] = docs[1][i]

        return render_template('index.html', context=contenuto["documento"],
                                id0=docs[1][0],id1=docs[1][1],id2=docs[1][2])

def isNotRequest(sentence):
    i = 0
    sentence = cleaning.prepare_sentence(sentence)
    altri = ['ulterior', 'risult','mostr', 'document', 'correl']
    for word in sentence:
        if(word in altri):
            i = i + 1
    prob = i / len(sentence)

    if(prob > 0.60):
        return True
    else:
        return False

@app.route("/servizio", methods=['GET'])
def servizio():
    id = request.args.get('id_doc')
    contenuto = documenti[int(id)]["servizio"]
    return render_template('index.html', context=contenuto,id0=id)

@app.route("/allegati", methods=['GET'])
def allegati():
    id = request.args.get('id_doc')
    contenuto = documenti[int(id)]["allegati"]
    contenuto = "".join(["  Allegato:  "+str(link) for link in contenuto])
    return render_template('index.html', context=contenuto,id0=id)

if __name__ == "__main__":
      #pred.restore_model("/app/Models/0601 080/model.tflearn",554,240)
      #cleaning.load_stopWord("/app/dataUtils/stop_words.txt")
      #documenti = pred.get_documents()

