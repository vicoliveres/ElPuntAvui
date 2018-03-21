# This is a template for a Python scraper on morph.io (https://morph.io)
# including some code snippets below that you should find helpful

#ElPuntAvui

#import libraries
import scraperwiki
import lxml.html
import urllib
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from lxml import html
from time import sleep

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
sleep(5)

#scrape table function
def scrape_mainpage(root):
    articles = root.cssselect("div.article")  # selects all <tr blocks in <table id="AutoNumber2"
    ref = 0
    
    for article in articles:
        # Set up our data record - we'll need it later
        record = {}
        ref = ref+1
        # grab all <td>s in the row
        title = article.cssselect("a")
        # if there are any <td>s:
        if title: 
            #grab the text contents of the first and put in 'record' under the key 'Rink':
            record['Title'] = title[0].text
            #grab the first href=" attribute (the URL of the link) and put into 'rinklink'
            articlelink = title[0].attrib.get('href')
            record['Link'] = articlelink
            #combine with base url and scrape into 'rinkhtml' 
            urllink = 'https://www.elperiodico.com'+articlelink
            articlehtml = requests.get(urllink, verify=False)
            #convert into lxml object and put into 'rinkroot'
            articleroot = html.fromstring(articlehtml.content)
            #grab all the <td><a> tags from 'rinkroot' and put into 'rinktds'
            articleauthor = articleroot.cssselect('span.createby')
            
            if articleauthor:
                record['Author'] = articleauthor[0].text
            # elif articleroot.cssselect('a.author-link'):
            #     record['Author'] = articleroot.cssselect('a.author-link')[0].text
            # else:
            #     record['Author'] = 'other'
            
            record['Media'] = 'ElPuntAvui'
            record['Ref'] = ref
           
        # Print out the data we've gathered
        print record, '------------'
        # Finally, save the record to the datastore - 'Rink' is our unique key
        scraperwiki.sqlite.save(["Title"], record)

base_url = 'http://www.elpuntavui.cat/barcelona.html'
starting_url = base_url
def scrape_and_look_for_next_link(url):
    page = requests.get(url, verify=False)
    root = html.fromstring(page.content)
    scrape_mainpage(root)

scrape_and_look_for_next_link(starting_url)

