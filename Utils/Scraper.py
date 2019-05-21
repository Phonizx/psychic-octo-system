import requests
from bs4 import BeautifulSoup
import re
import json
import time

intervallo_ids = [26146, 26149]
categoryIds = [26121, 26133, 380201]

def save_html(h,id):
    ids = str(id).replace(" ","")
    ids = ids.replace("/","-").replace(".","_").replace(",","_")
    html = "./html/Pagina"+ids+".html"
    
    with open(html,"w", encoding="utf-8")as f:
        f.write(h)
    f.close()
    return html

def download_page_cat():
    url_home = "http://www.comune.bari.it/web/egov/tutti-i-servizi?p_p_id=122_INSTANCE_PWQa78XYpDDH&p_r_p_564233524_categoryId="
    print("*")
    for id in categoryIds:
        print("."),
        url = url_home + str(id)
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html.parser')
        save_html(str(soup), id)

    for id in range(intervallo_ids[0],intervallo_ids[1]+1):        
        print("."),
        url = url_home + str(id)
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html.parser')
        save_html(str(soup),id)
    print("*")

def create_index_links(path, id_page,index):
    with open(path, "r", encoding='latin-1') as p:
        c=p.read()
        soup = BeautifulSoup( c,'html.parser')

        #retrive all the titles
        ul = soup.find_all("h4") 
        #retrive all the links
        links = soup.find_all(title=re.compile("Consulta la scheda"))

        print("num titoli: " + str(len(ul)) + " num links: " + str(len(links)))
    
        i=0
        for titolo in ul:
            link = links[i]["href"]
            index[titolo.text]=link
            i+=1
        p.close()

def create_index(path):
    index = {}
    for id in categoryIds:
        page = "./html/Pagina"+str(id)+".html"
        print(page)
        create_index_links(page,id,index)

    for id in range(intervallo_ids[0], intervallo_ids[1]+1):
        page = "./html/Pagina"+str(id)+".html"
        print(page)
        create_index_links(page,id,index)
        
    with open(path, "w", encoding='latin-1') as indx:
        indx.write(json.dumps(index))
    indx.close()

def clean(s):
    return s.replace('\n','').replace('\t','').replace("b'","").replace("'"," ").replace("b\"","")

#scrape info from html page
def scrape_page(page,id): 
    with open(page, "r", encoding='raw_unicode_escape') as f:
        c = f.read()
        soup = BeautifulSoup(c, 'html.parser')

        titolo = soup.find("div", {"class": "scheda-titolo"})
        sottotitoli = soup.find_all( "div", {"class": "accordion-heading"})
        inners = soup.find_all( "div", {"class": "accordion-inner"})

        i=0
        len_sottotitoli = len(sottotitoli)
        len_inners = len(inners)
        print("num sottitoli: "+ str(len_sottotitoli)+" num contenuti: "+str(len_inners))
        with open("DOC"+id+".txt","w") as fp:
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

#path of the index
def scraping(path):
    with open(path, encoding='raw_unicode_escape') as indice_file: #encoding="raw_unicode_escape"
        tmp = indice_file.read().encode('raw_unicode_escape').decode()
        indice = json.loads(tmp)       
        id = 1
        for titolo, url in indice.items(): 
            print(titolo+" "+url)
            r = requests.get(url) 
            if(r.status_code != 200):
                print("Errore"+str(r.status_code))
                time.sleep(20)
            soup = BeautifulSoup(r.content, 'html.parser')
            try:
                html = save_html(str(soup), titolo)            
                scrape_page(html, str(id))
            except:
                print("°°°°°°°°°°°°°°°°"+str(id)+"°°°°°°°°°°°°°°°°°°°°°°°°°°")
            id+=1
            time.sleep(2)


