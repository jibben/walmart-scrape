# Created by Jibben Hillen
# For L2 code test
# 2015-11-27

import urllib2
import json
import bs4
import re
import csv

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
def buildDict(page_soup, ranking):
    product = {}

    # get adContextJSON from page
    script = cheerios_soup.find("script", attrs={'id':'tb-djs-wml-base'})
    ad_context = re.search('(?<=\"adContextJSON\": ){.*}', script.string)
    ad_json = json.loads(ad_context.group(0))

    # get product name
    product["name"] = ad_json["query"].encode('ascii','replace')

    # insert ranking
    product["ranking"] = ranking

    # get price
    product["price"] = float(ad_json["price"])

    # get brand
    product["brand"] = ad_json["brand"].encode('ascii','replace')

    # get review info
    reviews = re.search('\d+ reviews \| \d.\d out of 5', page_soup.get_text())
    review_text = reviews.group(0).split()
    product["num_reviews"] = int(review_text[0])
    product["rating"] = float(review_text[3])

    return product

# function to build list from all page dictionaries
def buildList(soup):

    return cereal_list

# function to write given list of dicts to CSV
def listToCSV(list, fieldnames, filename):
    if(len(list[0]) != len(fieldnames)):
        raise ValueError('Number of fieldnames != Number of items in dict')

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for product in list:
            writer.writerow(product)

# main dictionary to hold data
#searches = {}

# first do cereal
# cereal_soup = getQuerySoup(BASE_URL, "cereal")

#url = urllib2.urlopen("http://www.walmart.com/ip/Honey-Nut-Cheerios-Gluten-Free-Cereal-26.6-oz/25847978")
file = open('cheerios.html')
cheerios_soup = bs4.BeautifulSoup(file.read(), "html.parser")
cheerios = buildDict(cheerios_soup, 1)
print cheerios
