# Google Scholar API

This repositary proposes a code to scrape through Google Scholar research informations and automatically download all available papers with their metadata. It was specifically designed to work on chemistry components research. This project won a Hackathon organized by Mines Nancy (Engineering School in France).

## Before running the code (WINDOWS)
* Install Google Chrome
* Download code and ressources folder
* Add the ressources folder to your PATH (https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/)
* (Open new cmd and type 'chromedriver' to check that the variable was added to path)
* Open cmd and execute (pip3 install -r ressources\requirements.txt) ou (pip3 install --user -r ressources\requirements.txt) if permissions are denied
* Or add manually the libraries :
  * bs4
  * selenium
  * fake_useragent
  * pathlib
  * requests
  * pubchempy
  * time, os, codecs, re, csv
* To make the notebook work, add the folowing :
  * ipywidgets
  * tkinter
  * IPython

## How to use
There are 2 ways to use this script : 
* Use the Jupyter Notebook Interface (recommended)
* Execute the "download_files" method of a Scraper() instance, directly from the Google_Scholar_API.py

## Variables of the Scraper
* download_dir : Directory where the files will be downloaded with the metadata csv
* language : 'fr', 'en'.. Language of Google, which switches reasearch results a little
* captcha : change to True if you get recognized as a bot and start to get the error "NoneType Element has no attribute findChildren". It will switch to a selenium webdriver to scrape html, and let you manually fill in the Captcha before you can keep going.
* sleeptime : time in seconds to wait for the pages to charge when downloading embedded pdfs or html pages. You may need to make it longer if you have a slow connexion to not get errors

## Future Extensions 
* Choose to export metadata in json or csv
* Add HTML sources other than sciencedirect
* Find a way to better treat the captchas issue
* Transform .pdf to good .html
* Treat .html file to ensure they are indeed related to the subject
