import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf

import numpy as np
import nltk
#from nltk.stemlancaster import LancasterStemmer
import json
import tflearn
import datetime

class Training:

    def __init__(self,path):
        self.path = path
        self.load_trainingset()

    def load_trainingset(self):
        self.train_x = np.load(self.path + "train_x.npy")
        self.train_y = np.load(self.path + "train_y.npy")
        self.create_model()

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
        self.model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
        return self.model

    def training(self,epochs = 1000):
        #model = self.create_model()
        self.model.fit(self.train_x, self.train_y, n_epoch=epochs, batch_size=50, show_metric=True)
        print("Save model? (n or y): ")
        res = input()
        if(res == 'y'):
            self.save_model(self.model)

    def save_model(self,model):
         save_path = "/home/phinkie/Scrivania/psychic-octo-system/Models/"
         dir = datetime.datetime.now().strftime('%m-%d|%H:%M')
         save_path += dir
         os.makedirs(save_path)
         model.save(save_path + '/model.tflearn')
         print("Model stored in: " + save_path)
         
path = "C:\\Nuova cartella\\psychic-octo-system\\"
mod = Training("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
mod.training(2000)
