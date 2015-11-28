# Created by Jibben Hillen
# For L2 code test
# 2015-11-27

import urllib2
import json
import bs4
import re
import csv
import pprint

# providing a variable with the base URL such that if the IP were to change it
# would remain easy to scrape website info
BASE_URL = "http://www.walmart.com"

# function to return a soup from a base and a query
def getQuerySoup(base, query):
    url = urllib2.urlopen(base + "/search/?query=" + query)
    soup = bs4.BeautifulSoup(url.read(), "html.parser")
    return soup

# function to return a soup from a base and page link
def get_page_soup(base, link):
    url = urllib2.urlopen(base + link)
    soup = bs4.BeautifulSoup(url.read(), "html.parser")
    return soup

# function to build dictionary for single page
def build_dict(page_soup, ranking):
    product = {}

    # get adContextJSON from page
    script = page_soup.find("script", attrs={'id':'tb-djs-wml-base'})
    ad_context = re.search('(?<=\"adContextJSON\": ){.*}', script.string)
    ad_json = json.loads(ad_context.group(0))

    # get product name
    product["name"] = ad_json["query"].encode('ascii','replace')

    # insert ranking
    product["ranking"] = ranking

    # get price
    product["price"] = float(ad_json["price"])

    # get brand
    # the data on walmart webpage is bad, so we have to try to
    # manually find the actual brand within the name of the product
    # and only if that fails will we try to scrape it from the page
    if "Kellogg's" in product["name"]:
        product["brand"] = "Kellogg's"
    elif "Post" in product["name"]:
        product["brand"] = "Post"
    elif "Kashi" in product["name"]:
        product["brand"] = "Kashi"
    elif "Cheerios" in product["name"]:
        product["brand"] = "Cheerios"
    elif "Lucky Charms" in product["name"]:
        product["brand"] = "General Mills"
    elif "Cinnamon Toast Crunch" in product["name"]:
        product["brand"] = "General Mills"
    else:
        brand = page_soup.find('span', attrs={'itemprop':'brand'}).string
        product["brand"] = brand.encode('ascii','replace')

    # get review info, first check if reviews exist
    no_reviews = page_soup.find("p", attrs={'class':'zero-reviews-summary'})
    if(no_reviews):
        product["num_reviews"] = 0
        product["rating"] = 0.0
    else:
        reviews = page_soup.find('div', attrs={'class':'Grid-col u-size-1-2 stars stars-large pull-left hide-content display-inline-block-m'})
        review_text = reviews.find('p', attrs={'class':'heading-e'}).string
        review_text = review_text.split()
        product["num_reviews"] = int(review_text[0])
        product["rating"] = float(review_text[3])

    return product

# function to build list from all page dictionaries
def build_list(soup):
    # initialize list to hold products
    product_list = []

    # get all products from page
    products = soup.find_all('h4', attrs={'class':'tile-heading'})

    # for each product, find url, get info, add to list
    rank = 1
    for prod in products:
        url = prod.find('a').get('href')
        prod_soup = get_page_soup(BASE_URL, url)
        prod_info = build_dict(prod_soup, rank)
        product_list.append(prod_info)
        rank += 1

    return product_list

# function to write given list of dicts to CSV
def listToCSV(list, fieldnames, filename):
    # send a traceback if number of items in dicts != number of field names
    if(len(list[0]) != len(fieldnames)):
        raise ValueError('Number of fieldnames != Number of items in dict')

    # write to file with DictWriter
    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for product in list:
            writer.writerow(product)

def main():
    # first do cereal
    cereal_soup = getQuerySoup(BASE_URL, "cereal")

    output = build_list(cereal_soup)

    pprint.pprint(output)

main()
