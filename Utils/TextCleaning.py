import nltk
from nltk.stem.snowball import SnowballStemmer
import os,glob
import re
import string
import json


#Cleaning iniziale da dare in pasto al PreEmbedder
class TextPreparation:

    tag = set()

    unique_words = set()
    vocab_size = 0

    word2int = {}
    int2word = {}

    stopWords = {}
    #no white-space, no dot
    puncts = ['!','?',',',';',':','(',')','-']


    def __init__(self,path):
        self.path = path
        #self.stemmer = SnowballStemmer("italian")
        self.stemmer = nltk.stem.snowball.ItalianStemmer()

    def no_punctuation(self,sentence): #erase puncts
        sentence = sentence.translate({ord(c) : '' for c in self.puncts})
        return sentence

    def load_stopWord(self,path):
        i = 0
        with open(path,"r") as fstopword:
            for line in fstopword:
                l = line.replace('\n','')
                if l not in self.stopWords.keys():
                    self.stopWords[l] = i
                    i += 1
        print("Stop Words loaded.")

    def build_dicts(self):
        if(self.vocab_size > 0):
            for i,word in enumerate(self.unique_words):
                self.word2int[word] = i
                self.int2word[i] = word
        self.save_dicts()

    def save_dicts(self):

        dizionari = []
        dizionari.append(self.word2int)
        dizionari.append(self.int2word)
        dizionari.append(self.vocab_size)

        dict_file = open(self.path + "/dizionari.json", "w")
        dict_file.write(json.dumps(dizionari))
        dict_file.close()
        print("Data writed in: " + self.path + "dizionari.json")

    def prepare_sentence(self, sentence):
        new_sent = []
        sentence = self.no_punctuation(sentence)
        #print(sentence)
        for token in sentence.split():
            if(token not in self.stopWords.keys() and token not in ' '):
                token = self.stemmer.stem(token)
                #if(token not in self.tag):
                new_sent.append(token)
                #self.tag.add(token)
        return new_sent

    def prepare_texts(self):
        os.chdir(self.path)
        for file in glob.glob("*.txt"):
            with open(file,"r") as f:
                print("Text PreProcessing on: " + file.title())
                sentences = []
                for line in f:
                    line = self.no_punctuation(line)
                    l = line.split()
                    for iword in l:
                        if(iword not in self.stopWords.keys()):
                            iword = self.stemmer.stem(iword)
                            self.unique_words.add(iword) #aggiunge una parola non stop-word e stemmata al set di parole globali
                            sentences.append(iword + " ") #stemming not stopwords

            with open(file,"w") as f:
                f.writelines(sentences)
        self.vocab_size = len(self.unique_words)
        self.build_dicts()

    def split_inWindow(self,win_size = 2,title=""):
        WINDOW_SIZE = win_size #win_size
        data = []
        for i in range(0,len(title)-1):
            data.append([title[i],title[i+1]])
        return data

    def labelling(self,pathdoc):
        with open(pathdoc,"r") as ds:
                doc = json.load(ds)
        empty = 0
        doc_empty = []

        document_tag = []
        for d in doc:
            titolo = d["documento"].split('Cosa')[0].strip().lower()
            title = self.prepare_sentence(titolo)
            tagged = self.split_inWindow(2,title)

            t = ""
            for i in range(0,len(tagged)):
                yo = ' '.join(tagged[i])
                if i == len(tagged)-1:
                    t = t + yo
                else:
                    t = t + yo + "|"
            if(t in ""):
                empty +=  1
                doc_empty.append(d["id"])
            d["titoli_univoci"] = t
            document_tag.append(d)
            #print(d)
            #print("\n\n\n\n")
        print("Documenti senza tag: " + str(empty))
        print(doc_empty)

    
        tag_file = open("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/docTag.json","w")
        tag_file.write(json.dumps(document_tag,indent=4))
        tag_file.close()

            #self.split_inWindow(2,title)


tp = TextPreparation("/home/phinkie/Scrivania/psychic-octo-system/data/")
tp.load_stopWord("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/stop_words.txt") #path
#tp.prepare_texts()

tp.labelling("/home/phinkie/Scrivania/psychic-octo-system/data/docs.json")
