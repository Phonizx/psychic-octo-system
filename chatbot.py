import os

from flask import Flask
from flask import request
from flask import redirect, url_for
from flask import render_template

from pymongo import MongoClient

from octosystem import predictor


app = Flask(__name__)

model = None

@app.route("/")
def home():
    pred = predictor("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
    model = pred.restore_model("/home/phinkie/Scrivania/tes/psychic-octo-system/Models/0601 080/model.tflearn",554,240)
    return "Model caricato !"
    '''
    path = "C:\\Nuova cartella\\psychic-octo-system\\"
    pred = predictor(path+"dataUtils\\")#("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
#"/home/phinkie/Scrivania/psychic-octo-system/
    model = pred.restore_model(path+"Models\\0601 080\\model.tflearn",554,240)
    return "Model caricato !"
    '''

@app.route("/test",methods=['POST','GET'])
def tester():
    if(request.method == 'GET'):
        data = request.args.get('Text')

        return render_template('index.html', context="Kitestramurt" + data)


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
