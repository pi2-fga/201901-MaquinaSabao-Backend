import requests
import re
from bs4 import BeautifulSoup as bs

lojas_americanas_url = requests.get("https://www.americanas.com.br/busca/detergente-liquido")

soup = bs(lojas_americanas_url.content, 'html.parser')

product_list = soup.select("div.product-grid-item > div:nth-child(1)")

cheaper_product = {'item_description':'','item_volume':1,  'item_price':100}

for item in product_list:
    item_name = item.get('name')
    item_volume = None
    if item.select_one("div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > section:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)"):
        item_price = float(re.search(r'R\$\s*(\d{1,5}\,\d{1,2})', item.select_one("div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > section:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)").text).group(1).replace(',','.'))

    if re.search(r'((\d{1,4})\s*(ml|ML|Ml|Litros|litros|L|l))', item_name):
        if re.search(r'((\d{1,4})\s*(ml|ML|Ml|Litros|litros|L|l))', item_name).group(3) in ['Litros','litros','L','l']:
            item_volume = float(re.search(
                r'((\d{1,4})\s*(ml|ML|Ml|Litros|litros|L|l))', item_name).group(2))*1000
        else:
            item_volume = float(re.search(r'((\d{1,4})\s*(ml|ML|Ml|Litros|litros|L|l))', item_name).group(2))
        
    if (item_name and item_price and item_volume) and ((item_price/item_volume) < (cheaper_product['item_price']/cheaper_product['item_volume'])):
        cheaper_product['item_description'] = item_name
        cheaper_product['item_volume'] = item_volume
        cheaper_product['item_price'] = item_price

print(cheaper_product)
