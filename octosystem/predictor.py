import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf

import numpy as np
import tflearn
import json

class predictor:
    def __init__(self,path):
        self.path = path
        self.load_data()

    def get_classes(self):
        return self.classes

    def getdocumentById(self, id):
        return self.documents[int(id)-1]["documento"]

    def load_data(self):
        with open(self.path + "words.json") as wordsFile:
            wf = json.load(wordsFile)
            self.words = wf[0]
            #self.classes = wf[2]

        with open(self.path + "docTag.json") as docFile:
            self.documents = json.load(docFile)

    def get_documents(self): #return all documents 
        return self.documents

    def bow(self,sentence): #da  stemmatizzare , eliminare le stopwords e la punteggiatura
        # tokenize the pattern
        sentence_words = sentence.replace("!","").split(' ')
         # bag of words
        bag = [0]*len(self.words)
        i=0
        for s in sentence_words:
            #w = stemmer.stem(s)
            if(s in self.words):
                    for i,w in enumerate(self.words):
                            if w == s:
                                    bag[i] = 1
        bag = np.array([bag])
        bag = bag.astype(np.float32)
        return bag


    def restore_model(self,model_path,input_dim,output_dim):
        tf.reset_default_graph()
        # Input Layer
        net = tflearn.input_data(shape=[None, input_dim])
        #Hidden Layers con 20 hidden units
        net = tflearn.fully_connected(net, 20)
        net = tflearn.fully_connected(net, 20)
        #Outpu Layer con fn. activation softmax
        net = tflearn.fully_connected(net, output_dim, activation='softmax')
        net = tflearn.regression(net)
        self.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

        self.model.load(model_path)
        return self.model

    def prediction(self,sentence):
        pred = self.model.predict(self.bow(sentence))
        docs = (-pred).argsort()[-3:]
        docs_corr = []
        for i in range(0,3):
            docs_corr.append(docs[0][i])
        #print(self.getdocumentById(docs_corr[0]))
        #print(docs_corr)
        return docs_corr


#/home/phinkie/Scrivania/psychic-octo-system/Models/05-30|17:38/model.tflearn model bk
#pred = predictor("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
#model = pred.restore_model("/home/phinkie/Scrivania/psychic-octo-system/Models/0601 080/model.tflearn",554,240) #vocabSize, lenClasses
#print(pred.prediction("cors nuot"))
