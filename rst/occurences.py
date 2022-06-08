from io import StringIO

import csv

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import pubchempy as pcp

#function which return a list of synonym for a given name of a molecule or a given pubchem number

def synonyms(mol):

    if type(mol)==int:
        molecule = pcp.Compound.from_cid(mol)
        return molecule.synonyms
    elif type(mol)==str:
        molecule = pcp.get_compounds(mol, 'name')
        return(molecule[0].synonyms)
    else: return ("Veuillez entrer un nom de molécule ou un numéro de référence pubchem svp")

#return a text of str type with the pdf content

def ToText(file): #file is a filname (str) or a path

    output_string = StringIO()
    with open(file, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return output_string.getvalue()


# file : #pdf file (str) or path
# mol : a given name of a molecule or a given pubchem number
def Occurences(file, mol):

    text = ToText(file)
    
    OccTot = 0
    for synonym in synonyms(mol):
        word = ' '+mol+' '
        occ = text.count(word)
        OccTot +=occ
        occ = 0
    return OccTot

def pertinence(liste_pdf,recherche):
    Dico = dict()
    file = open('Occurences.csv','w',newline='')
    for pdf in liste_pdf:
        Dico[pdf] = Occurences(pdf,recherche)
        ecrire=csv.writer(file, delimiter=';')
        ecrire.writerow([pdf, Dico[pdf] ]) 

    return Dico

liste = ['bonjour.pdf', 'coucou.pdf', 'salut.pdf']
pertinence(liste,'rutin')



   
 









        

