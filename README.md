# Google Scholar API

This repositary proposes a code to scrape through Google Scholar research informations and automatically download all available papers with metadata.

## Before running the code (WINDOWS)
* Install Google Chrome
* Download code and ressources folder
* Add the ressources folder to your PATH (https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)
* (Open new cmd and type 'chromedriver' to check that the variable was added to path)
* Open cmd and execute (pip3 install -r ressources\requirements.txt)
* Or add manually the libraries :
  * bs4
  * selenium
  * fake_useragent
  * pathlib
  * requests
  * time, os, codecs, re, csv

## How to use
There are 2 ways to use this script : 
* Use the Jupyter Notebook
* Execute the "pages_infos" function directly from the Google_Scholar_API.py

## Global Variables
* DOWNLOAD_DIR : Directory where the files will be downloaded with the metadata csv
* LANGUAGE : 'fr', 'en'.. Language of Google, which switches reasearch results a little
* CAPTCHA : change to True if you get recognized as a bot and start to get errors like "NoneType Element has no attribute findChildren". It will switch to a selenium driver to scrape html, and let you manually fill in the Captcha.
* SLEEP : time in seconds to wait for the pages to charge when downloading embedded pdfs. You may need to make it longer if you have a slow connexion to not get errors
