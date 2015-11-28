# walmart-scrape
Scrape search results for given keywords for L2 Coding challenge

Created by Jibben Hillen

This python script will scrape through the first page of a Walmart query and extract data about the products displayed. It has been coded to work for cereals (the only hard-coding for this revolves around brand labeling, because Walmart's database doesn't have very good brand labeling), but it should generally work for any given walmart search.

For this application, scraping is used due to potential limitations of Walmart's free API (5 requests per second and 5k requests per day). This scraping platform can easily be scaled up to take any number of keywords through an implementation of reading keywords from a csv and will automatically work for any number of brands (although this is slightly iffy because of Walmart's bad brand labeling).

Usage:
python walmart_scrape.py \<keyword\> \<optional additional keywords\> ... \<output filename\>

For every given keyword, the program will scrape the first page of Walmart search and save the data in the output file chosen. For this reason, searches must be in a single string (using + instead of space, etc).
If no additional commands are given, the script will just run for "cereal" and "cold cereal" and save the output to "walmart.csv"

The following data are collected:
"query", "date", "ranking", "brand", "name", "price", "num_reviews", "rating"
