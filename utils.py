import json
import re

class utils:
    def __init__(self):
        pass

    word2index = {}
    index2word = {}

    def build_dicts(self,path):
        pad_id = 0
        start_id = 1
        oov_id = 2
        index_offset =  2
        with open(path + "/dataset.txt") as ds:
            i =   index_offset
            for line in ds:
                tokens = line.replace('\n','').split()
                for t in tokens:
                    if not(t in self.word2index.keys()):
                        self.word2index[t] = i
                        i+=1
            self.index2word = {v + index_offset: k for k, v in self.word2index.items()}
            self.index2word[0] = "PAD"
            self.index2word[1] = "START"
            self.index2word[2] = "OOV"
            print(self.word2index)
            print(self.index2word)
            #self.write_dicts(path)

    def write_dicts(self,path_write):
        dict_file = open(path_write + "/dizionari.json", "a")
        dict_file.write(json.dumps(self.word2index))
        dict_file.write(json.dumps(self.index2word))
        dict_file.close()


tool = utils()
tool.build_dicts("/home/phinkie/Scrivania/psychic-octo-system")
