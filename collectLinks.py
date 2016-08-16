#Collect a list of Wikipedia links to all American TV shows

from bs4 import BeautifulSoup as soup
import pandas as pd
import re
from urllib import request
 
def soupTheLink(url):
    html = request.urlopen(weblink).read().decode('utf8')
    return soup(html, 'lxml')

def collectLinks(url):
    souped = soupTheLink(url)
    
    showLinks = []
    
    for listItem in souped.find_all('li'):
        link = listItem.find('a', href = True)
        try:
            fullLink = 'https://en.wikipedia.org' + link['href']
            showLinks.append(fullLink)
        except TypeError:
            pass
    showLinks = showLinks[28:2282]
    return showLinks