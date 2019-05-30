import json
import numpy as np


class dataPrepare:

    training_data = []
    documents = []
    classes = []
    words = set()

    class_index = 'id'
    sentence_index = 'Titolo'
    vocab_size = 0

    def __init__(self,path): #path documento del
        self.path = path
        self.load_data()


    def load_data(self):
        with open(self.path,"r") as docs:
            dataset = json.load(docs)
            try:
                for row in dataset:
                    data = {}
                    data[self.sentence_index] = row["titoli_univoci"].split('|')
                    data[self.class_index] = row["id"]
                    self.training_data.append(data)
                print("Loaded data in: " + self.path)
            except:
                print("Loading data error")

    def processing_data(self):
        for p in self.training_data:
            for sente in p["Titolo"]:
                pm = sente.replace("!","").lower().split(' ')
                self.words.update(pm)
                self.documents.append((pm, p[self.class_index]))
            if p[self.class_index] not in self.classes:
                    #print(p[class_index])
                    self.classes.append(p[self.class_index])
        self.vocab_size = len(self.words)
        self.create_ds()


    def create_ds(self):
        print("Creating dataset ...")
        training_x =[]
        output_empty = [0] * len(self.classes)
        output_y = []
        for doc in self.documents:
            bag = []
            pw = doc[0]
            for sw in self.words:
                if(sw in pw):
                    bag.append(1)
                else:
                    bag.append(0)

            training_x.append(bag)
            output_row = list(output_empty)
            output_row[self.classes.index(doc[1])] = 1
            output_y.append(output_row)
        self.train_x = np.array(training_x)
        self.train_y = np.array(output_y)


    def save_ds(self,savePath):
        lobj = []
        lobj.append(list(self.words))
        lobj.append(self.vocab_size)


        wordsFile = open(savePath + "words.json", "w")
        wordsFile.write(json.dumps(lobj))
        wordsFile.close()

        #salvataggio a parte delle classi 
        classFile = open(savePath + "classes.json","w")
        classFile.write(json.dumps(self.classes))
        classFile.close()
        try:
            np.save(savePath + "train_x" ,self.train_x)
            np.save(savePath + "train_y" ,self.train_y)
            print("Train_x and Train_y are stored in: " + savePath)
        except:
            print("Stored error in " + savePath)

prepare = dataPrepare("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/docTag.json")
prepare.processing_data()
prepare.save_ds("/home/phinkie/Scrivania/psychic-octo-system/dataUtils/")
