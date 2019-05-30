import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf

import numpy as np
import nltk
#from nltk.stemlancaster import LancasterStemmer
import json
import tflearn


with open("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/" + "words.json","r") as filewords:
    fw =  json.load(filewords)
    words = fw[0]
    vocab_size = fw[1]
    classes = fw[2]
train_x = np.load("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/" + "train_x.npy")
train_y = np.load("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/" + "train_y.npy")


def bow(sentence, words, show_details=False):
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


def create_model():
    tf.reset_default_graph()
    # Input Layer
    net = tflearn.input_data(shape=[None, len(train_x[0])])
    #Hidden Layers con 20 hidden units
    net = tflearn.fully_connected(net, 20)
    net = tflearn.fully_connected(net, 20)
    #Outpu Layer con fn. activation softmax
    net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
    net = tflearn.regression(net)
    model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
    return model

#load_data("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
model = create_model()
model.fit(train_x, train_y, n_epoch=1000, batch_size=50, show_metric=True)
#model.save('model.tflearn')

pred = model.predict(bow("mortal concession",words)) #2

#sorted_array = np.sort(pred)
#reverse_array = sorted_array[::-1]

print(classes[np.argmax(pred)]) # + " Prob: \t" + str(pred))
#print(reverse_array[:3])

pred = model.predict(bow("rit civil",words)) #3
print(classes[np.argmax(pred)]) #+ " Prob: \t" + str(pred))

#print(classes[np.argmax(model.predict(bow("talk to you yolo",words)))])
#print(classes[np.argmax(model.predict(bow("can you make",words)))])
