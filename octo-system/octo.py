import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf

import numpy as np
import nltk
#from nltk.stemlancaster import LancasterStemmer
import json
import tflearn


class Training:
    def __init__(self,path):
        self.path = path
        self.load_trainingset()

    def load_trainingset(self):
        with open(self.path + "words.json","r") as filewords:
            fw =  json.load(filewords)
            self.words = fw[0]
            self.vocab_size = fw[1]
            self.classes = fw[2]
        self.train_x = np.load(self.path + "train_x.npy")
        self.train_y = np.load(self.path + "train_y.npy")


    def bow(self,sentence, words, show_details=False):
        # tokenize the pattern
        sentence_words = sentence.replace("!","").split(' ')
         # bag of words
        bag = [0]*len(words)
        i=0
        for s in sentence_words:
            #w = stemmer.stem(s)
            if(s in words):
                    for i,w in enumerate(words):
                            if w == s:
                                    bag[i] = 1
        bag = np.array([bag])
        bag = bag.astype(np.float32)

        return bag

    #linear classificator
    def create_model(self):
        tf.reset_default_graph()
        # Input Layer
        net = tflearn.input_data(shape=[None, len(self.train_x[0])])
        #Hidden Layers con 20 hidden units
        net = tflearn.fully_connected(net, 20)
        net = tflearn.fully_connected(net, 20)
        #Outpu Layer con fn. activation softmax
        net = tflearn.fully_connected(net, len(self.train_y[0]), activation='softmax')
        net = tflearn.regression(net)
        model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        return model

    def training(self):
        model = self.create_model()
        model.fit(self.train_x, self.train_y, n_epoch=1000, batch_size=50, show_metric=True)
        print("Save model? ")
        res = input()
        if(res == 'y'):
            model.save('model.tflearn')
            print("Model stored in current path.")
        




mod = Training("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
mod.training()


#pred = model.predict(bow("mortal concession",words)) #2

#sorted_array = np.sort(pred)
#reverse_array = sorted_array[::-1]

#print(classes[np.argmax(pred)]) # + " Prob: \t" + str(pred))
#print(reverse_array[:3])

#pred = model.predict(bow("rit civil",words)) #3
#print(classes[np.argmax(pred)]) #+ " Prob: \t" + str(pred))

#print(classes[np.argmax(model.predict(bow("talk to you yolo",words)))])
#print(classes[np.argmax(model.predict(bow("can you make",words)))])
