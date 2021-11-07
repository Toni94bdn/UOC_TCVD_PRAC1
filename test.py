import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import re

soup= BeautifulSoup(req.get("https://catala.habitaclia.com/lloguer-barcelona.htm").content, 'html.parser')
items = soup.find_all("div", {"class": "list-item-info"})
result = []
for citem in items:
    price = citem.find('span', itemprop = 'price').text
    price = re.sub(r'[^\d]+|[\.]','',price)
    location = citem.find('p', {'class' : 'list-item-location'}).span.text
    features = citem.find('p', {'class' : 'list-item-feature'}).text
    surface = re.findall("\d+", features)[0]
    rooms = re.findall("\d+", features)[2]
    bathrooms = re.findall("\d+", features)[3]
    surfprice = re.findall("[\d+\,\.]+", features)[4]
    premium = False
    if (len(citem.find('div', {'class' : 'list-item-premium'}).text)!= 0):
        premium = True
    updt_date = citem.find('span', {'class' : 'list-item-date'}).text
    updt_date = re.sub(r'[^\d]','',updt_date)

    result.append(
        {
            'location':location,
            'surface':surface,
            'rooms':rooms,
            'bathrooms':bathrooms,
            'surface_price_rate':surfprice,
            'premium?':premium,
            'update_date':updt_date,
            'price': price
        }
    )
result_df = pd.DataFrame(result) 
print(result_df)

