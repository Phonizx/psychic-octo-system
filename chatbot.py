import os

from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template

from pymongo import MongoClient

app = Flask(__name__)


client = MongoClient("128028d9c08b",27017)
db = client.docDb



@app.route("/")
def home():
    return "Testing on !"

@app.route("/create")
def create():
    doc = {
        'Id' : 999,
        'Documento' : "test documento su mongodb",
        "Allegati" : "url allegati",
        "Servzio" : "url servizio",
        "Titoli_univoci": "Tag documento"
    }
    db.docDb.insert_one(doc)
    return "ok"

@app.route("/cerca")
def cerca():
    find_docs = db.docDb.find()
    docs = [item for item in find_docs]
    return render_template('index.html', context=docs)

@app.route("/test",methods=['POST','GET'])
def tester():
    if(request.method == 'GET'):
        data = request.args.get('Text')
        return render_template('index.html', context="Kitestramurt" + data)


'''
@app.route("/create")
def home():
    doc = {
        'Id' : 999,
        'Documento' : "test documento su mongodb",
        "Allegati" : "url allegati",
        "Servzio" : "url servizio",
        "Titoli_univoci": "Tag documento"
    }
    db.docDb.insert_one(doc)


'''





if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
