#!/usr/bin/env python
# coding: utf-8

# Import dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
from flask import Flask, render_template
from flask_pymongo import PyMongo
import time

# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# Define database and collection
db = client.mars_db
collection = db.items

def init_browser():
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ## NASA Mars News

def scrape():
url = "https://mars.nasa.gov/news/"
browser.visit(url)


html = browser.html
soup = bs(html, "html.parser")


# Recent news title
headline = soup.select_one("div.list_text")
news_title = headline.find("div", class_="content_title").text.strip()
news_title


# Recent news paragraph 
news_p = headline.find("div", class_="article_teaser_body").text.strip()
news_p


# ## NASA Images: Mars from Space

jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"
browser.visit(f"{jpl_url}index.html")


html = browser.html
soup = bs(html, "html.parser")


featured_image= soup.select_one("img.headerimage")


featured_image_url = f"{jpl_url}{featured_image['src']}"
featured_image_url


# ## Mars Facts

url = "https://space-facts.com/mars/"


facts = pd.read_html(url)
facts


# Scraping facts table
fact_df = facts[0]
fact_df


# Converting fact table to html
html_table = fact_df.to_html()
html_table


# ## Mars Hemisphere

url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
browser.visit(url)
time.sleep(1)
soup = bs(browser.html, "html.parser")


hemi_item = soup.find_all('div', class_="item")
urls = []
for item in hemi_item:
    marsPic = item.find('a')['href']
    hemi_url = 'https://astrogeology.usgs.gov' + marsPic
    urls.append(hemi_url)
print(urls)    


# Store data in a dictionary
    marsNASA_data = {
        "article_title": news_title,
        "article_para": news_p,
        "pic_url": featured_image_url,
        "mars_facts": html_table,
        "hemi_pics": hemi_url
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return marsNASA_data
