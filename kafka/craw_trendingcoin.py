import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine
import time

def convert_float(s,ud):
    if s=='up':
        return round(float(ud),7)
    elif "--" in ud:
        return 0
    else:
        return round(float(ud)*-1,7)
    
def replace_starting_with_zero(price):
    if price.startswith("0.0.."):
        return 0.000000001
    else:
        return  round(float(price),7)

def convert_marketcap_to_bigint(marketcap_raw):
    # if marketcap_raw.endswith("T"):
    #     return int(float(marketcap_raw[:-1]) * 1_000_000_000_000)  # Convert Trillion to Billion
    # elif marketcap_raw.endswith("B"):
    #     return int(float(marketcap_raw[:-1]) * 1_000_000_000)  # Convert Billion to Billion
    # elif marketcap_raw.endswith("M"):
    #     return int(float(marketcap_raw[:-1]) * 1_000_000)  # Convert Million to Billion
    # elif marketcap_raw.endswith("K"):
    #     return int(float(marketcap_raw[:-1]) * 1_000)  # Convert Thousand to Billion
    # else:
    marketcap_raw.replace("$", "").replace(",", "")
    marketcap_value = ''.join(filter(str.isdigit, marketcap_raw))
    return marketcap_value.replace(".", "")


def crawl_trending_coin():
    result = requests.get('https://coinmarketcap.com')
    content = result.text
    soup = BeautifulSoup(content,"html")
    trending_coin = []
    list_coin=soup.find("tbody").find_all("tr")
    for index, coin in enumerate(list_coin[:10]):
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        name = coin.find_all("td")[2].find_all("div")[1].find("p").get_text()
        symbol = coin.find_all("td")[2].find_all("div")[2].find_all("p")[1].get_text()
        price =replace_starting_with_zero(coin.find_all("td")[3].find("span").get_text()[1:].replace(",", ""))
        ud24h=coin.find_all("td")[4].find("span").get_text()[:-1]
        s24h=coin.find_all("td")[4].find_all("span")[1].attrs.get("class")[0].split("-")[2]
        ud7d=coin.find_all("td")[5].find("span").get_text()[:-1]
        s7d=coin.find_all("td")[5].find_all("span")[1].attrs.get("class")[0].split("-")[2]
        ud30d=coin.find_all("td")[6].find("span").get_text()[:-1]
        s30d=coin.find_all("td")[6].find_all("span")[1].attrs.get("class")[0].split("-")[2]
        marketcap = convert_marketcap_to_bigint(coin.find_all("td")[7].get_text()[1:].replace(",", ""))
        # marketcap = coin.find_all("td")[7].get_text()[1:].replace(",", "").replace("$", "")
        volume24h = coin.find_all("td")[8].find_all("p")[0].get_text()[1:].replace(",", "")
        coin_info = {"rank":list_coin.index(coin)+1,"name":name,"symbol":symbol,"price":price,"_24h_percent":convert_float(s24h,ud24h),"_7d_percent":convert_float(s7d,ud7d),"_30d_percent":convert_float(s30d,ud30d),"marketcap":int(marketcap),"volume24h":int(volume24h),"updated_at":time}
        trending_coin.append(coin_info)
    return trending_coin

