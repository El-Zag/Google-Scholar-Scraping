
#****************************************************************
#Telechargement d'un pdf à dans le répertoire courant à partir d'un fichier .pdf, avec le nom 
# lien entre simple apostrophe
#nom entre double apostrophe


import urllib.request




lien = 'https://www.tandfonline.com/doi/pdf/10.1080/12538078.1997.10515791'
nom = "nom2.html"

def telecharge(lien, nom):

    urllib.request.urlretrieve(lien,nom) 


telecharge(lien, nom)