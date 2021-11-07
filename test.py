import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import re

soup= BeautifulSoup(req.get("https://catala.habitaclia.com/lloguer-barcelona.htm").content, 'html.parser')
items = soup.find_all("div", {"class": "list-item-info"})
result = []
for citem in items:
    try:
        price = citem.find('span', itemprop = 'price').text
    except:
        price = ''
    price = re.sub(r'[^\d]+|[\.]','',price)
    #-----------------------------------------------
    try:
        location = citem.find('p', {'class' : 'list-item-location'}).span.text
    except:
        location = ''
    #-----------------------------------------------
    try:
        features = citem.find('p', {'class' : 'list-item-feature'}).text
    except:
        features = ''
    #-----------------------------------------------
    try:
        surface = re.findall("\d+", features)[0]
    except IndexError:
        surface = ''  
    #-----------------------------------------------
    try:
        rooms = re.findall("\d+", features)[2]
    except IndexError:
        rooms = ''
    #-----------------------------------------------
    try:
        bathrooms = re.findall("\d+", features)[3]
    except IndexError:
        bathrooms = ''
    #-----------------------------------------------
    try:
        surfprice = re.findall("[\d+\,\.]+", features)[4]
    except IndexError:
        surfprice = ''
    #-----------------------------------------------
    premium = False
    if (citem.find('div', {'class' : 'list-item-premium'}).text.upper().rfind('PREMIUM')>0):
        premium = True
    updt_date = citem.find('span', {'class' : 'list-item-date'}).text
    updt_date = re.sub(r'[^\d]','',updt_date)
    if(len(updt_date)<=0):
        updt_date = 0
    result.append(
        {
            'location':location,
            'surface':surface,
            'rooms':rooms,
            'bathrooms':bathrooms,
            'surface_price_rate':surfprice,
            'premium?':premium,
            'days_from_last_update':updt_date,
            'price': price
        }
    )
result_df = pd.DataFrame(result) 
print(result_df)

