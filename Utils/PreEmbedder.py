import numpy as np
import glob,os 
import json 


class PreEmbedder: #ama cambie nom 
    path = ""
    
    word2int = {}
    int2word = {}

    sentences = [] #list of sentences 
    set_words = {} #set of words in each documents 
    vocab_size = 0
    data = [] #splitted word in a window [2]

    x_train = [] # input word
    y_train = [] # output word
    
    def __init__(self,path):
        self.path = path

    def get_corpora(self):
        os.chdir(self.path)
        g = glob.glob("*.*")
        for file in glob.glob("*.txt"):
            with open(file) as f:
                for line in f:
                    self.set_words.update(line.split())
                    raw_sentences = line.split('.')
                    self.sentences.append(raw_sentences)
        self.vocab_size = len(self.set_words)
        #return a set of word and sentences in each documents 

    def build_dicts(self): #create two dicts for mapping words 
        if(self.vocab_size > 0):
            for i,word in enumerate(self.set_words):
                self.word2int[word] = i
                self.int2word[i] = word

    def split_inWindow(self,win_size = 2):
        WINDOW_SIZE = win_size
        for sentence in self.sentences:
            for word_index, word in enumerate(sentence):
                for nb_word in sentence[max(word_index - WINDOW_SIZE, 0) : min(word_index + WINDOW_SIZE, len(sentence)) + 1] :
                    if nb_word != word:
                        self.data.append([word, nb_word])
    
    def to_one_hot(self,data_point_index, vocab_size):
        temp = np.zeros(self.vocab_size)
        temp[data_point_index] = 1
        return temp

    def create_dataSet(self):
        for data_word in self.data:
            self.x_train.append(self.to_one_hot(self.word2int[data_word[0]], self.vocab_size))
            self.y_train.append(self.to_one_hot(self.word2int[data_word[1]], self.vocab_size))
        # convert them to numpy arrays
        self.x_train = np.asarray(self.x_train)
        self.y_train = np.asarray(self.y_train) 
    
    def save_data(self):
        np.save("x_train",self.x_train)
        np.save("y_train",self.y_train)
        dizionari = []
        dizionari.append(self.word2int)
        dizionari.append(self.int2word)

        dict_file = open(self.path + "/dizionari.json", "a")
        dict_file.write(json.dumps(dizionari))
        dict_file.close()