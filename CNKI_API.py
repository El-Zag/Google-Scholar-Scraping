import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium import Keys
from time import sleep
from sys import platform
import os
import codecs
from pathlib import Path
import re
from fake_useragent import UserAgent
import csv


class Scraper:
    def __init__(self, download_dir, language, captcha, sleeptime, overseas=False):
        # Parameters that can be altered during the session
        self.download_dir = download_dir
        self.language = language
        self.captcha = captcha # Does CNKI ever make you do a captcha?
        self.sleep = sleeptime

        # Global parameters
        self.regex = re.compile('[^a-zA-Z0-9]')
        self.ua = UserAgent()
        self.headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600',
            'User-Agent': self.ua.random,
        }

        self.driver = None

        if overseas:
            self.url = "https://oversea.cnki.net/"
            self.overseas = True
        else:
            self.url = "https://cnki.net/"
            self.overseas = False

        if self.captcha:
            options = webdriver.ChromeOptions()
            options.add_argument(f'user-agent={self.ua.random}')
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(self.url)


        if platform == "win32":
            self.slash = '\\'
        if platform == "linux" or platform == "linux2" or platform == "darwin":
            self.slash = '/'

    def set_language(self, language):
        self.language = language

    def set_download_dir(self, download_dir):
        self.download_dir = download_dir

    def set_captcha(self, captcha):
        if not (self.captcha == captcha):
            if self.captcha:
                self.driver.close()
                self.driver = None
            else:
                self.driver = webdriver.Chrome()
                self.driver.get(self.url)

    def set_sleep(self, sleeptime):
        self.sleep = sleeptime

    # searchbar should be a String, just as you would have typed it in CNKI
    # downloaded the documents related to the searchbar String, for the pages indicated
    # returns a list of dics with the metadata
    def scrape_all(self, search, authors=[], first_page=1, last_page=5, include_all = False):

        articles_dl = []

        if isinstance(authors, str):
            authors = [authors]

        # make search query manually
        search_main = self.driver.find_element_by_class_name("search-main")
        search_input = search_main.find_element_by_id("txt_search")
        search_input.send_keys(search)
        search_input.send_keys(Keys.RETURN)
        search_input.submit()

        for i in range(first_page, last_page + 1):

            print("\nExploration of Page " + str(i))

            soup_page = BeautifulSoup(driver.page_source, "html.parser")
            article = self.page_scraper(soup_page)

            articles_dl = articles_dl + article

            # Is there another page?
            if soup_page.find("div", class_="pages", id='PageNext') is not None:
                if i != (last_page+1):
                    pages_class = self.driver.find_element_by_class_name("pages")
                    pagenext_button = pages_class.find_element_by_id("PageNext")
                    pagenext_button.click()


        print("\n" + str(len(articles_dl)) + " documents available")
        return articles_dl

    # Scrape each page one at a time
    def page_scraper(self, soup_page):
        if not self.captcha:
            req = requests.get(soup_url, self.headers)
            soup = BeautifulSoup(req.content, 'lxml')

        # SWITCH TO THIS if captcha block
        else:
            self.driver.get(soup_url)
            soup = BeautifulSoup(self.driver.page_source, 'lxml')

        # All the results of the page
        results = soup.find("div", id="gs_res_ccl_mid")

        # List of all the articles
        articles = results.findChildren("div", class_="odd")

        articles_dl = []
        # TODO: I want to eventually rewrite this section/inputs so that instead of include_all,
        # we have a flag download=Y/N, and another one to ignore ones missing the doc (ignore_missing?)
        for article in articles:
            info = self.article_info(article)
            articles_dl.append(info)

# TODO: rewrite this/trace through?                self.save_metadata(info)

        return articles_dl

    # Take as input a div class = "gs_r gs_or gs_scl" (an article in google scholar's html)
    # With a downloadable link (assert)
    # Output is a dictionary with those infos :
    # { Title : String, title of the paper,
    # Link : String, url to the article,
    # Authors : Dict of authors and profile links (if available)
    # Journal : List, partial name of Journal and link
    # Date : String, Year-Month-Day of publication
    # Source : String, Source of publication
    # Summary : String, abstract (optional, future)
    # Cited : Int, Number of times cited (optional, future)
    # Download : String, url to download the text (optional, future)
    # DOI : String (optional, future)
    # Source : String, website the download is from}
    def article_info(self, soup_article):
        # assert (soup_article.find("div", class_="gs_ggs gs_fl") is not None, "Il n'y a pas de lien pour télécharger cet article")
        info = dict()

        # Informations sur l'article
        name_class = soup_article.findChild("div", class_="name")
        info['Title'] = name_class.a.text
        info['Link'] = name_class.a['href']

        authors = dict()
        author_class = soup_article.findChildren("div", class_="author")
        for author in author_class:
            authors[author.a.text] = author.a['href']
        info['Authors'] = authors

        source_class = soup_article.findChildren("div", class_="source")
        info['Source'] = [source_class.a.text, source_class.a['href']]

        info['Year'] = soup_article.findChildren("div", class_="date").text

# This would be nice but it seems like we'd have to scrape the subpage, see note below
#        info['Journal'] = publication_infos[2]

# Can this be removed?
#        summary = general_infos.findChild("div", class_="gs_rs").text
#        summary = summary.replace(u'\xa0', u' ')

        # The CNKI summary is not available from the search page; we'd have to spawn
        # off a new thread/tab for each article and scrape it from there. TODO: Add
        # this as an optional feature
# TODO        info['Summary'] = summary
#        info['Cited'] = cited[5:len(cited) - 5]

#        if has_document:
#            dl_infos = soup_article.findChild("div", class_="gs_or_ggsm")
#            info['Download'] = dl_infos.a['href']
#            if dl_infos.text == "Full View":
#                info['Type'] = 'HTML'
#                info['DL Source'] = 'unknown'
#            else:
#                dl_type = dl_infos.span.text
#                info['Type'] = dl_type[1:len(dl_type) - 1]
#                info['DL Source'] = dl_infos.a.text.split(']')[1].split()[0]
        return info

    def most_recent_file(self):
        files = os.listdir(self.download_dir)
        if not files:
            return 0
        paths = [os.path.join(self.download_dir, basename) for basename in files]
        file = max(paths, key=os.path.getctime)
        return file


    def save_metadata(self, info):
        exists = os.path.isfile(self.download_dir + self.slash + 'metadonnees.csv')
        with open(self.download_dir + self.slash + 'metadonnees.csv', 'a', newline='', encoding="utf-8") as output:
            dictwriter = csv.DictWriter(output, fieldnames=info.keys(), delimiter=";")
            if not exists:
                dictwriter.writeheader()
            dictwriter.writerow(info)
            output.close()

