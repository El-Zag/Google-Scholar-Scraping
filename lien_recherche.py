# Ce code affiche le lien d'une page de recherche q dans google scholar (sous forme de chaine de caractère entre simples appostrophes) 


import requests

headers_Get = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def recherche_google_scholar(mots):


    q = '+'.join(mots.split())

    #effectue une recherche dans google research avec les mots spécifiés dans q
    r = requests.get('https://scholar.google.com/scholar?hl=fr&as_sdt=0%2C5&q='+ q + '&btnG=', headers=headers_Get)

    #URL de la page de recherche
    url = r.url #chaîne de caractère
    return url



print (recherche_google_scholar('monoxyde carbone'))


