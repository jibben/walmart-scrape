# Created by Jibben Hillen
# For L2 code test
# 2015-11-28

import urllib2              # to construct url file-like objects
import json                 # to interpret json
import bs4                  # for BeautifulSoup to scrape easier
import re                   # regex parsing html
import csv                  # to write output at csv
import os.path              # to check if file exists for writing output
from datetime import date   # to put date on output
import sys                  # to get command line inputs

BASE_URL = "http://www.walmart.com"
FIELDS = ["query", "date", "ranking", "brand", "name",
          "price", "num_reviews", "rating"]

# function to return a soup from a base and page link
def get_soup(base, link):
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
def build_list(soup, query):
    # initialize list to hold products
    product_list = []

    # get all products from page
    products = soup.find_all('h4', attrs={'class':'tile-heading'})

    # for each product, find url, get info, add to list
    rank = 1
    for prod in products:
        url = prod.find('a').get('href')
        prod_soup = get_soup(BASE_URL, url)
        prod_info = build_dict(prod_soup, rank)
        prod_info["query"] = query
        prod_info["date"] = date.today().strftime("%Y-%m-%d")
        product_list.append(prod_info)
        rank += 1

    return product_list

# function to write given list of dicts to CSV
def list_to_CSV(list, fieldnames, filename):
    # send a traceback if number of items in dicts != number of field names
    if(len(list[0]) != len(fieldnames)):
        raise ValueError('Number of fieldnames != Number of items in dict')

    # create flag whether to write header (only if new file)
    # we will assume that any previous files will have been made by this program
    if(not os.path.isfile(filename)):
        write_header = True
    else:
        write_header = False

    # write to file with DictWriter
    with open(filename, 'a') as f:
        writer = csv.DictWriter(f, fieldnames = fieldnames,
                                quoting=csv.QUOTE_NONNUMERIC)

        if(write_header):
            writer.writeheader()

        for product in list:
            writer.writerow(product)

def main():

    num_args = len(sys.argv)
    # if no additional arguments are given, pretend as if the following are:
    # walmart_scrape.py cereal cold+cereal walmart.csv
    if(num_args == 1):
        # first do for cereal
        soup = get_soup(BASE_URL, "/search/?query=cereal")
        products = build_list(soup, "cereal")
        list_to_CSV(products, FIELDS, "walmart.csv")

        # then for cold cereal
        soup = get_soup(BASE_URL, "/search/?query=cold+cereal")
        products = build_list(soup, "cold+cereal")
        list_to_CSV(products, FIELDS, "walmart.csv")

    # if usage incorrect print and exit
    elif(num_args == 2):
        print("Usage: " + sys.argv[0] + " <keyword>" +
              " <additional keywords> ... <output filename>")
        exit()

    else:
        # for every search given, do scraping and add to CSV given
        for i in range(0,num_args - 2):
            soup = get_soup(BASE_URL, "/search/?query=" + sys.argv[i+1])
            products = build_list(soup, sys.argv[i+1])
            list_to_CSV(products, FIELDS, sys.argv[num_args-1])

main()
