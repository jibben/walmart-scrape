# walmart-scrape
Scrape search results for given keywords for L2 Coding challenge
Created by Jibben Hillen

This python script will scrape through walmart queries and extract data about the product. It has been coded to work for cereals (the only hard-coding for this revolves around brand labeling, because Walmart's database doesn't have very good brand labeling), but it should generally work for any given walmart search.

Usage:
python walmart_scrape.py <keyword> <optional additional keywords> ... <output filename>

For every given keyword, the program will scrape the first page of walmart search and save the data in the output file chosen. For this reason, searches must be in a single string(using + instead of space, etc).
If no additional commands are given, the script will just run for "cereal" and "cold cereal" and save the output to "walmart.csv"

The following data are collected:
"query", "date", "ranking", "brand", "name", "price", "num_reviews", "rating"
