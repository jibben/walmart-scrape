# Created by Jibben Hillen
# For L2 code test
# 2015-11-27

import urllib2
import json
import bs4

# providing a variable with the base URL such that if the IP were to change it
# would remain easy to scrape website info
BASE_URL = "http://www.walmart.com/search/?query="

# function to return a soup from a base and a query
def getQuerySoup(base, query):
    url = urllib2.urlopen(base + query)
    soup = bs4.BeautifulSoup(url.read(), "html.parser")
    return soup

# function to return a soup from a base and page link
def getPageSoup(base, link):
    url = urllib2.urlopen(base + urllib2.quote(link.get('href')))
    soup = bs4.BeautifulSoup(url.read(), "html.parser")
    return soup

# function to build dictionary for single page
def buildDict(pageSoup):

    return cereal

# function to build list from all page dictionaries
def buildList(soup):

    return cereal_list


# main dictionary to hold data
searches = {}

# first do cereal
cereal_soup = getSoup(BASE_URL, "cereal")
