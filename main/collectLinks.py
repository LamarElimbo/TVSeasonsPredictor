#Collect a list of Wikipedia links to all American TV shows

from bs4 import BeautifulSoup as soup
import re
from urllib import request
import settings
import pandas as pd
import os
 
def soupTheLink(url):
    html = request.urlopen(url).read().decode('utf8')
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


def main():
    mainUrl = 'https://en.wikipedia.org/wiki/List_of_American_television_series'
    links = collectLinks(mainUrl)
    for link in links:
        settings.WIKI_LINKS['link'].append(link)
        
    df = pd.DataFrame(settings.WIKI_LINKS, columns = settings.LINK_COLUMNS)
    os.chdir('..')
    os.chdir(settings.DATA_DIR)
    print(df.head())
    df.to_csv(settings.LINKS_FILE)
    
if __name__ == "__main__":
    main()