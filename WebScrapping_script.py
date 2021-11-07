#Toni Forcada
import requests as req
from bs4 import BeautifulSoup
import pandas as pd
import re


def main(in_url):
    page = readPage(in_url)
    soup= getSoup(page)
    nItems = readNitems(soup)
    nItemsPerPage = readNitemsPage(soup)
    result = []
    for idPage in range(0, (nItems//nItemsPerPage) + 1):
        cURL = set_cPageURL(in_url,idPage)
        print(cURL)
        cPage = readPage(cURL)
        if cPage is None:
            break
        cSoup= getSoup(cPage)
        cItems = readItemsPage(cSoup)
        result = readItemsInfo(cItems,result)
    result_df = pd.DataFrame(result) 
    result_df.to_csv('results.csv')
    del result
    print(result_df)

def readPage(in_url):
    out_page = req.get(in_url)
    if(out_page.status_code != 200):
            out_page = NULL
    return out_page
def readNitemsPage(in_soup):
    out_NitemsPage = len(in_soup.find_all("div", {"class": "list-item"}))
    return out_NitemsPage

def readItemsPage(in_soup):
    out_AitemsPage = in_soup.find_all("div", {"class": "list-item-info"})
    return out_AitemsPage
   
def readNitems(in_Soup):
    out_Nitems = in_Soup.find(id='id_numInm_Formalerta')
    return int(out_Nitems['value'])

def getSoup(in_Page):
    out_Soup = BeautifulSoup(in_Page.content, 'html.parser')
    return out_Soup
def set_cPageURL(in_initialURL, in_idPage):
    out_cURL = in_initialURL
    if(in_idPage != 0):
        out_cURL = out_cURL.replace(".htm","-"+str(in_idPage)+".htm")
    return out_cURL

def readItemsInfo(in_itemsList,result):
    for citem in in_itemsList:
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
        #-----------------------------------------------
        updt_date = citem.find('span', {'class' : 'list-item-date'}).text
        updt_date = re.sub(r'[^\d]','',updt_date)
        if(len(updt_date)<=0):
            updt_date = 0
        #-----------------------------------------------
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
    return result
main("https://catala.habitaclia.com/lloguer-barcelona.htm")