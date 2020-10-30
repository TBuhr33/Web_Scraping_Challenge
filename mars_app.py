from flask import Flask, redirect, render_template
from flask_pymongo import PyMongo
from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri = "mongodb://localhost:27017/mars_app")

@app.route('/')
def index():
    data = mongo.db.collection.find_one()
    return render_template('index.html', mars_data = data)
    
@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert = True)
    return redirect ('/')

if __name__ == '__main__':
    app.run(debug = True)
