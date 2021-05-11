import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import os
import codecs
from pathlib import Path
import re
from fake_useragent import UserAgent
import csv

# To simulate a real user and not a bot

UA = UserAgent()

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': UA.random,
}

# Path to directory where texts will be downloaded
DOWNLOAD_DIR = os.getcwd() + "\\Download"

# Language of google (not the papers). Will change the results a bit
# Put fr or en to switch between french and english google
LANGUAGE = 'fr'

# If the search is being blocked by Captchas, change this to True
CAPTCHA = False
if CAPTCHA:
    DRIVER = webdriver.Chrome()
    DRIVER.get("https://scholar.google.com/")

# Time to sleep between embedded downloads, in seconds
SLEEP = 7

# Transform characters to save pdfs names
REGEX = re.compile('[^a-zA-Z0-9]')


# Take as input a div class = "gs_r gs_or gs_scl" (an article in google scholar's html)
# With a downloadable link (assert)
# Output is a dictionary with those infos :
# { Title : String, title of the paper,
# Link : String, url to the article,
# Authors : String, list of Authors
# Journal : String, partial name of Journal
# Year : int, Year of publication
# Source : String, Source of publication
# Summary : String, Google scholar summary
# Cited : Int, Number of times cited
# Download : String, url to download the text
# Type : String, 'PDF', 'HTML'..}
def article_info(soup_article):
    # assert (soup_article.find("div", class_="gs_ggs gs_fl") is not None, "Il n'y a pas de lien pour télécharger cet article")
    info = dict()

    # Informations sur l'article
    general_infos = soup_article.findChild("div", class_="gs_ri")
    info['Title'] = general_infos.h3.a.text
    info['Link'] = general_infos.h3.a['href']

    publication_infos = general_infos.findChild("div", class_="gs_a").text
    publication_infos = publication_infos.replace(u'\xa0', u' ')
    publication_infos = publication_infos.split(" - ")
    length = len(publication_infos[1])
    info['Authors'] = publication_infos[0]
    info['Journal'] = publication_infos[1][0:length - 6]
    info['Year'] = int(publication_infos[1][length - 4:length])
    info['Source'] = publication_infos[2]

    summary = general_infos.findChild("div", class_="gs_rs").text
    summary = summary.replace(u'\xa0', u' ')
    info['Summary'] = summary

    bottom_text = general_infos.findChild("div", class_="gs_fl")
    cited = bottom_text.findChildren("a")[2].text
    cited = cited.replace(u'\xa0', u' ')
    info['Cited'] = cited[5:len(cited) - 5]

    # Informations sur le téléchargement
    dl_infos = soup_article.findChild("div", class_="gs_or_ggsm")
    info['Download'] = dl_infos.a['href']
    dl_type = dl_infos.span.text
    info['Type'] = dl_type[1:len(dl_type) - 1]

    return info


# downloads all the available texts from the google scholar url
def url_infos(soup_url):
    if not CAPTCHA:
        req = requests.get(soup_url, HEADERS)
        soup = BeautifulSoup(req.content, 'lxml')

    # SWITCH TO THIS if captcha block
    else:
        DRIVER.get(soup_url)
        soup = BeautifulSoup(DRIVER.page_source, 'lxml')

    # All the results of the page
    results = soup.find("div", id="gs_res_ccl_mid")

    # List of all the articles
    articles = results.findChildren("div", class_="gs_r gs_or gs_scl")

    # Articles with a downloadable link
    articles_dl = []
    for article in articles:
        if article.find("div", class_="gs_ggs gs_fl") is not None:
            info = article_info(article)
            # Cas d'un lien pdf directement
            if info['Type'] == 'PDF':

                # Name of the file we're going to download
                name = REGEX.sub('_', info['Title'].lower()) + '.pdf'

                # Check if the paper has already been downloaded
                if not os.path.exists(DOWNLOAD_DIR + '\\' + name):
                    info['Filename'] = name

                    # If the link is already a pdf file, download it directly
                    if os.path.splitext(info['Download'])[1] == ".pdf":
                        filename = Path(DOWNLOAD_DIR + '\\' + name)
                        response = requests.get(info['Download'])
                        filename.write_bytes(response.content)

                    # If not, use webdriver to download the links
                    else:
                        dl_embedded_pdf(info['Download'], name)
                    print(info)
                    articles_dl.append(info)

                    exists = os.path.isfile(DOWNLOAD_DIR + '\\metadonnees.csv')
                    with open(DOWNLOAD_DIR + '\\metadonnees.csv', 'a', newline='', encoding="utf-8") as output:
                        dictwriter = csv.DictWriter(output, fieldnames=info.keys(), delimiter=";")
                        if not exists:
                            dictwriter.writeheader()
                        dictwriter.writerow(info)
                        output.close()

    return articles_dl


# Downloads pdfs that are embedded in a link and not .pdf
# Uses additional selenium and time for Wiley documents
def dl_embedded_pdf(link, name):
    options = webdriver.ChromeOptions()

    options.add_experimental_option('prefs', {
        "download.default_directory": DOWNLOAD_DIR,  # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not show PDF directly in chrome
    })
    options.add_argument(f'user-agent={UA.random}')

    driver = webdriver.Chrome(options=options)
    driver.get(link)

    sleep(SLEEP)

    # For pdfs from wiley it doesn't download it right away
    frame = driver.find_elements_by_id('pdf-iframe')
    if len(frame) == 1:
        driver.switch_to.frame(frame[0])
        driver.find_element_by_tag_name('a').click()
        sleep(SLEEP)

    files = os.listdir(DOWNLOAD_DIR)
    paths = [os.path.join(DOWNLOAD_DIR, basename) for basename in files]
    file = max(paths, key=os.path.getctime)
    os.rename(file, DOWNLOAD_DIR + '\\' + name)
    driver.close()


# Generate the google scholar url based on the words in the searchbar, at the indicated page
def generate_url(searchbar, page=1):
    q = searchbar.split()
    for i in range(len(q)):
        if not q[i].isalpha():  # For characters that aren't letters, they are encoded in hex by google
            if q[i] == "\\":
                q[i] = "%5C"
            else:
                q[i] = codecs.encode(bytes(q[i], 'utf-8'), 'hex')
                q[i] = codecs.decode(q[i], 'utf-8')
                q[i] = '%' + q[i].upper()
    q = '+'.join(q)
    page = (page - 1) * 10
    return "https://scholar.google.com/scholar?start=" + str(page) + "&q=" + q + "&hl=" + LANGUAGE + "&as_sdt=0,5"


# downloaded the documents related to the search, for the pages indicated
# returns a list of dics with the metadata
def pages_infos(searchbar, first_page=1, last_page=5):
    articles_dl = []
    for i in range(first_page, last_page + 1):
        print("exploration de la page " + str(i))
        url = generate_url(searchbar, page=i)
        articles_dl = articles_dl + url_infos(url)
    return articles_dl

# searchbar = 'rutin'
# articles_downloaded = pages_infos(searchbar, 1, 5)
