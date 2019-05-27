import requests
import os
from bs4 import BeautifulSoup
import re
import json
import time
MAX_CHAR_KEY = 60
def clean(s):
    return s.replace('\n','').replace('\t','').replace("b'","").replace("'"," ").replace("b\"","")

class Scraper:
    
    url_home = ""
    intervallo_ids = []# [26146, 26149]
    categoryIds = []#[26121, 26133, 380201]

    def __init__(self, url):
        self.intervallo_ids = [26146, 26149]
        self.categoryIds = [26121, 26133, 380201]
        self.url_home = url

    def save_html(self, h, id):
        try:
            os.chdir("../Utils/html")
        except:
            print("",end="")
        ids = str(id).replace(" ","")
        ids = ids.replace("/","-").replace(".","_").replace(",","_")
        
        html = "Pagina" + ids + ".html"
        with open(html,"w", encoding="utf-8")as f:
            f.write(h)
        f.close()
        return html

    # def download_page_home(self):
    #     print("Downloading all page categories...")         
    #     r = requests.get(url_home)
    #     soup = BeautifulSoup(r.content, 'html.parser')
    #     s = self.save_html(str(soup), "home")
    #     print("Done.")
    #     return s

    
    def download_page_cat(self):
        try:
            os.makedirs("./html")
            os.chdir("../Utils/html")
        except FileExistsError:
            print("")

        print("Downloading all page categories...")
        for id in self.categoryIds:
            print(".", end="")
            url = url_home + str(id)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            self.save_html(str(soup), id)

        for id in range(self.intervallo_ids[0], self.intervallo_ids[1]+1):        
            print(".", end="")
            url = url_home + str(id)
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            self.save_html(str(soup), id)
        print("Done.")

    #path file html single page
    def create_index_links(self, path, id_page, index):

        with open(path, "r", encoding='latin-1') as p:
            c = p.read()
            soup = BeautifulSoup(c, 'html.parser')

            #retrive all the titles
            ul = soup.find_all("h4") 
            #retrive all the links
            links = soup.find_all(title=re.compile("Consulta la scheda"))

            print("num titoli: " + str(len(ul)) + " num links: " + str(len(links)))
        
            i=0
            for titolo in ul:
                t = str(titolo.text.encode("ascii","ignore"))
                t = t.replace(":","_").replace(".","-").replace("\\","-")
                link = links[i]["href"]
                index[t[:MAX_CHAR_KEY]] = link
                i+=1
            p.close()

    def create_index(self, path_json):
        index = {}
        os.chdir("./html")
        for id in self.categoryIds:
            # ./html/
            page = "Pagina" + str (id) + ".html"
            print(page)
            self.create_index_links(page, id, index)

        for id in range(self.intervallo_ids[0], self.intervallo_ids[1] + 1):
            page = "Pagina" + str(id) + ".html"
            print(page)
            self.create_index_links(page, id, index)
            
        with open(path_json+"index.json", "w", encoding='latin-1') as indx:
            indx.write(json.dumps(index))
        indx.close()

    # scrape info from html page
    def scrape_page(self, page, id): 
        try:
            os.makedirs("./docs")
            os.chdir("docs")
        except FileExistsError:
            print("", end="")

        with open(page, "r", encoding='raw_unicode_escape') as f:
            c = f.read()
            soup = BeautifulSoup(c, 'html.parser')
            servizio = soup.find("div", {"class":"scheda-online text-center"})
            print(type(servizio))#.find("a"))#["href"])
            titolo = soup.find("div", {"class": "scheda-titolo"})
            sottotitoli = soup.find_all( "div", {"class": "accordion-heading"})
            inners = soup.find_all( "div", {"class": "accordion-inner"})

            i=0
            len_sottotitoli = len(sottotitoli)
            len_inners = len(inners)
            print("num sottitoli: "+ str(len_sottotitoli)+" num contenuti: "+str(len_inners))
            with open("./docs/DOC"+id+".txt","w") as fp:
                fp.write("TITOLO:"+str(titolo.text.encode("utf-8")))
                fp.write("\n")
                for i in range(0,len_sottotitoli-1):                
                    fp.write("SOTTOTITOLO:")
                    fp.write(clean(sottotitoli[i].text).replace(" ",""))
                    fp.write("\n")
                    fp.write("CONTENUTO:")
                    contenuto = str(inners[i].text.encode("utf-8"))
                    c = clean(str(contenuto))
                    fp.write(c)
                    if len(c) == 0:
                        time.sleep(123)
                    fp.write("\n")
                    #print(clean_escape(sottotitoli[i].text).replace(" ",""))    
                    #print(clean_escape(inners[i].text).encode("utf-8"))
                    i+=1
            fp.close()
        f.close()
        
        try:
            os.chdir("..")
        except FileExistsError:
            print("", end="")

    def clean_title(self, t):
        return t.replace("b\'  ","").replace("  \'","")
    # #path_json of the index
    def scraping(self, path_json):
        with open(path_json, encoding='raw_unicode_escape') as indice_file:
            tmp = indice_file.read().encode('raw_unicode_escape').decode()
            indice = json.loads(tmp            )
            id = 1
            for titolo, url in indice.items():
                t = self.clean_title(titolo)
                print("TITOLO: "+ t + " URL:" + url)

                r = requests.get(url) 
                if(r.status_code != 200):
                    print("Errore"+str(r.status_code))
                    time.sleep(20)
                soup = BeautifulSoup(r.content, 'html.parser')
                html = self.save_html(str(soup), t) 
                print(html)
                # try:
                self.scrape_page(html, str(id))
                # except:
                    # print("Errore in scrape_page o in save_html alla pagina : '"+str(id)+"'")
                id+=1
                time.sleep(2)
 

url_home = ""
scraper = Scraper(url_home)
# scraper.download_page_cat() #working
path_json = "./html/index.json"
# scraper.create_index(path_json) #working
page = "D:\\a università\\terzo anno\\secondo semestre\\Sistemi ad agenti\\psychic-octo-system\\Utils\\html\\PaginaCAMBIODESTINAZIONEDUSODIIMMOBILE_RICHIESTADELPERM.html"
page = "D:\\a università\\terzo anno\\secondo semestre\\Sistemi ad agenti\\psychic-octo-system\\Utils\\html\\PaginaCERTIFICATODIDESTINAZIONEDUSODIIMMOBILE.html"
scraper.scrape_page(page,"10")
# scraper.scraping(path_json)
