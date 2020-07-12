#!/usr/bin/env python3
#-*- coding: utf-8 -*-
"""
Created on Thu Jun 25 18:16:42 2020
@author: pariya
"""
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
#import requests
#import time

#%%----------- Execute path to initialize Chromedriver ----------#
def init_browser():

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

#%% Define scraper and dictionary
def scrape_all():
    
    mars_scraper = {}
    
    mars_scraper["news_title"] = news()
    mars_scraper["news_p"] = news()
    mars_scraper["featured_image_url"] = featured_image()
    mars_scraper["mars_weather"] = weather()
    mars_scraper["mars_html"] = facts()
    mars_scraper["mars_hemispheres"] = hemispheres()

    return mars_scraper

#%%--------------- NASA Mars News ------------------------------
def news():
    # Visit the NASA Mars News Site
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    # Parse Results HTML with BeautifulSoup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    try:
        # Scrape the lastest news 'title'
        article = soup.find_all('div', class_='content_title')
        news_title = article[1].get_text()
        # Scrape the description text underneath
        news_p = article.find("div", class_ ="article_teaser_body").get_text()

    except AttributeError: 

        return news_title, news_p
    
#%%------------ JPL Mars Space Images - Featured Imag ----------
def featured_image():
    # Visit the NASA JPL site
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    
    #html = browser.html
    #soup = BeautifulSoup(html, "html.parser")
    
    # Find 'FULL IMAGE' button and Click on it
    full_image_button = browser.find_by_id('full_image')
    full_image_button.click()
    # Find 'more info' button and Click on it
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_button = browser.find_link_by_partial_text("more info")
    more_info_button.click()
    # Find a partial-href on the current page and pull out its 'href'
    featured_image = browser.links.find_by_partial_href('largesize')
    featured_image_url = featured_image['href']
    
    return featured_image_url
    
#%%--------------- Mars Weather from Twitter ---------------
def weather():
    # Visit the Mars Weather Twitter Account
    twt_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twt_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    ## Find all divs that contain tweets
    divs = soup.find_all('div', class_='css-901oao r-hkyrab r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0')

    # Loop thru each div and extract 'text' from its 'span' tag
    for target in divs:
    
        mars_weather = divs.find('span', class_='css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text[:-1]
    
        return mars_weather

#%%-------------------- Mars Facts --------------------
def facts():
    # Visit the Mars Facts Site
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    # Use pandas to read html
    fact_table = pd.read_html(facts_url)
    # Extract only Mars --> [0] not any other planets
    mars_df = fact_table[0]
    mars_df.columns=["Description", "Value"]
    mars_df.set_index("Description", inplace=True)
    # Ask to return the HTML strings? maybe
    mars_html = mars_df.to_html(header = False, index = False)
    
    return mars_html

#%%----------------- Mars Hemisphereres -----------------
def hemispheres():
    # Visit the USGS Astrogeology Science Center Site
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)

    html = browser.html
    #soup = BeautifulSoup(html, "html.parser")
    
    # Retreive all items that contain mars hemispheres information
    divs = soup.find("div", class_ = "result-list" )
    hemispheres = divs.find_all("div", class_="item")
    
    mars_hemispheres = []
    
    for hemi in hemispheres:
    
        title = hemi.find("h3").text
    
        link = hemi.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + link 
    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
    
        div_downloads = soup.find("div", class_="downloads")
        image_url = div_downloads.find("a")["href"]
        mars_hemispheres.append({"title": title, "img_url": image_url})
    
    return mars_hemispheres

#%%
if __name__ == "__main__":
    print(scrape_all())

