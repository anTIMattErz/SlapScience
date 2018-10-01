#import packages
import os
import urllib.request
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import pandas as pd
import datetime
from itertools import product
import re

#Class with webscraping driver based on api url
scraper_class = open("scraper_class.py", 'r').read()
exec(scraper_class)

#Class managing catalogue dataframes
catalogue_class = open("catalogue_class.py", 'r').read()
exec(catalogue_class)

#set working directory where you'll be saving data and name of data file in store or to create

os.chdir("c:\\Users\Yuri D'Agosto\Desktop\Scraping\SlapScience")

catalogue_name = "sc_hot_and_top.csv"

#==============================================================================
#===CHARTS URLS
#charts will be new and top and for each available country and genre
api_types = ["top", "new"]

countries = ['AU', 'CA', 'FR', 
             'DE', 'IE', 'NL', 
             'NZ', 'GB', 'US', 
             'all-countries']

genres = ['alternativerock', 'ambient', 'classical',
              'country', 'danceedm', 'dancehall',
              'deephouse', 'disco', 'drumbass',
              'dubstep', 'electronic','folksingersongwriter',
              'all-music', 'all-audio']
			  
#generate all combinations of api type, genre, and country
api_genre_country_combos = list(product(api_types, genres, countries))

#==============================================================================