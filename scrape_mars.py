from splinter import Browser
from bs4 import BeautifulSoup as bs
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd
import requests

def scrape():

    #MARS NEWS
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    html = browser.html
    news_soup = bs(html, "html.parser")

    news_title = news_soup.find_all("div", class_ = "content_title")[1].text
    news_p = news_soup.find("div", class_ = 'article_teaser_body').text

    #JPL IMAGES
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    jpg_soup = bs(html, "html.parser")

    jpg_container = jpg_soup.find("div", class_="carousel_items")
    image_url = jpg_container.find("article")["style"]

    url_clean = image_url.split("'")[1]

    jpl_base_url = "https://www.jpl.nasa.gov"
    feat_image_url = jpl_base_url + url_clean

    #print(feat_image_url)

    #MARS WEATHER
    #ryan helped me and talked me through this code to not use
    #big repetitive "css..." classes i kept finding on twitter
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    twit_soup = bs(response.text, 'html.parser')
    mars_w = twit_soup.find_all('p', class_="TweetTextSize")
    for tweet in mars_w:
        tweet.find('a').extract()
        if 'InSight sol' in tweet.text:
            mars_weather = tweet.text
            break
    mars_weather
    
   
    #MARS FACTS
    url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(url)
    mars_table = mars_table[0]
    mars_table.columns = ["Parameter", "Value"]
    mars_table
    mars_Tstring = mars_table.to_html()
    mars_Tstring

    #HEMISPHERES
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    hemi_soup = bs(response.text, 'html.parser')
    hemi_img_urls = []
    hemi_dict = {}

    hemispheres = hemi_soup.find_all('div', class_="description")

    #splinter through 
    for hemisphere in hemispheres:
        title = hemisphere.text
        browser.visit(url)
        browser.click_link_by_partial_text(title)
        html = browser.html
        hemi_soup_img = bs(html, 'html.parser')
        img_url = hemi_soup_img.find('li').a['href']
        
        hemi_dict["title"] = title
        hemi_dict["img_url"] = img_url
        
        hemi_img_urls.append(hemi_dict)
        hemi_dict = {}

    scrape_output = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": feat_image_url,
        "mars_weather": mars_weather,
        "mars_facts": mars_Tstring,
        "hemispheres": hemi_img_urls
    }
    return scrape_output

#print("run-it")