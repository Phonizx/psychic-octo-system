import requests
from bs4 import BeautifulSoup
'''
    Eventi della vita
http://www.comune.bari.it/web/egov/tutti-i-servizi?p_p_id=122_INSTANCE_PWQa78XYpDDH&p_r_p_564233524_categoryId=26121
    Tipologia utente
http://www.comune.bari.it/web/egov/tutti-i-servizi?p_p_id=122_INSTANCE_PWQa78XYpDDH&p_r_p_564233524_categoryId=26133
    Tipologia servizio
http://www.comune.bari.it/web/egov/tutti-i-servizi?p_p_id=122_INSTANCE_PWQa78XYpDDH&p_r_p_564233524_categoryId=26146
(fino)
http://www.comune.bari.it/web/egov/tutti-i-servizi?p_p_id=122_INSTANCE_PWQa78XYpDDH&p_r_p_564233524_categoryId=26149
    Modalita Fruizione Servizio
http://www.comune.bari.it/web/egov/tutti-i-servizi?p_p_id=122_INSTANCE_PWQa78XYpDDH&p_r_p_564233524_categoryId=380201








'''
intervallo_ids = [26146, 26149]
categoryIds = [26121, 26133, 380201]
def save_html(h,id):
    with open("./html/Pagina"+str(id)+".html","w")as f:
        f.write(h)
    f.close()

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

#<ul id="listaEntries">



#TEST
page = "./html/Pagina"+str(categoryIds[0])+".html"

soup = BeautifulSoup(open(page),'html.parser')

#retrive list entries
ul = soup.find_all("ul", { "id" : "listaEntries" })
ul_s = str(str(ul).encode("ascii","ignore"))

print(ul_s.replace("<>","\n"))
