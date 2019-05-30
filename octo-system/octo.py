
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf


import numpy as np
import nltk
from nltk.stem.lancaster import LancasterStemmer
import json
import tflearn


training_data = []

with open("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/docTag.json","r") as docs:
    dataset = json.load(docs)
    for row in dataset:
        data = {}
        data["Titolo"] = row["titoli_univoci"].split('|')
        data["id"] = row["id"]
        training_data.append(data)




documents = []
classes = []
words = set()

class_index = 'id'
sentence_index = 'Titolo'



stemmer = LancasterStemmer()

for p in training_data:
        for sente in p["Titolo"]:
            pm = sente.replace("!","").lower().split(' ')
            #w = [stemmer.stem(_w) for _w in pm]
            words.update(pm)
            documents.append((pm, p[class_index]))
        if p[class_index] not in classes:
                #print(p[class_index])
                classes.append(p[class_index])




def bow(sentence, words, show_details=False):
        # tokenize the pattern
        sentence_words = sentence.replace("!","").split(' ')
        # bag of words
        bag = [0]*len(words)
        i=0
        for s in sentence_words:
                w = stemmer.stem(s)
                if(w in words):
                        for i,w in enumerate(words):
                                if w == s:
                                        bag[i] = 1

        bag = np.array([bag])
        bag = bag.astype(np.float32)

        return bag

training = []
output_empty = [0] * len(classes)
output = []

for doc in documents:
        bag = []
        pw = doc[0]
        #print(pw)
        for sw in words:
                if(sw in pw):
                        bag.append(1)
                else:
                        bag.append(0)
        training.append(bag)

        output_row = list(output_empty)
        output_row[classes.index(doc[1])] = 1
        output.append(output_row)



train_x = np.array(training)
train_y = np.array(output)

print(len(train_y[0]))


#print(train_x)
#print(train_y)

'''



tf.reset_default_graph()
# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 20)
net = tflearn.fully_connected(net, 20)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)
# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
# Start training (apply gradient descent algorithm)
model.fit(train_x, train_y, n_epoch=1000, batch_size=50, show_metric=True)
#model.save('model.tflearn')
def bow(sentence, words, show_details=False):
        # tokenize the pattern
        sentence_words = sentence.replace("!","").split(' ')
         # bag of words
        bag = [0]*len(words)
        i=0
        for s in sentence_words:
            w = stemmer.stem(s)
            if(w in words):
                    for i,w in enumerate(words):
                            if w == s:
                                    bag[i] = 1
        bag = np.array([bag])
        bag = bag.astype(np.float32)

        return bag

pred = model.predict(bow("mortal concession",words)) #2
sorted_array = np.sort(pred)
reverse_array = sorted_array[::-1]

print(classes[np.argmax(pred)]) # + " Prob: \t" + str(pred))
print(reverse_array[:3])

pred = model.predict(bow("rit civil",words)) #3
print(classes[np.argmax(pred)]) #+ " Prob: \t" + str(pred))

#print(classes[np.argmax(model.predict(bow("talk to you yolo",words)))])
#print(classes[np.argmax(model.predict(bow("can you make",words)))])
'''
