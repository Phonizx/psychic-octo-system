import nltk
from nltk.stem.snowball import SnowballStemmer
import os,glob
import re
import string 


class TextPreparation:

    stopWords = {}
    #no white-space, no dot
    puncts = ['!','?',',',';',':']

    def __init__(self,path):
        self.path = path

    def load_stopWord(self,path):
        i = 0
        with open(path,"r") as fstopword:
            for line in fstopword:
                l = line.replace('\n','')
                if l not in self.stopWords.keys():
                    self.stopWords[l] = i
                    i += 1
        

    def no_punctuation(self,sentence):
        sentence = sentence.translate({ord(c) : '' for c in self.puncts})
        return sentence

    def prepare_texts(self):
        os.chdir(self.path)
        g = glob.glob("*.*")
        for file in glob.glob("*.txt"):
            with open(file,"r") as f:
                sentences = []
                for line in f:
                    line = self.no_punctuation(line)
                    l = line.split()
                    for iword in l:
                        if(iword not in self.stopWords.keys()):  
                            sentences.append(iword + " ")
                   
            with open(file,"w") as f:
                f.writelines(sentences)
#testing
tp = TextPreparation("/home/phinkie/Scrivania/psychic-octo-system/data/")
tp.load_stopWord("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/stop_words.txt") #path 
tp.prepare_texts()


 