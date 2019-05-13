import requests
import re
from bs4 import BeautifulSoup as bs

# lojas_americanas_url = requests.get(
#     "https://www.americanas.com.br/busca/soda-caustica")

# soup = bs(lojas_americanas_url.content, 'html.parser')

# product_list = soup.select("div.product-grid-item > div:nth-child(1)")

# for item in product_list:
#     item_name = item.get('name')
#     item_price = str(item.select_one(
#         "div.ColUI-sc-1ey7nd2-0 > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > section:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)").text)
#     item_weight = 0
#     item_concentration = str(re.search(r'9(8|9)\%', item_name))
#     if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name) and re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(3) == ("G" or "g"):
#         item_weight = float(re.search(
#             r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))/100
    
#     elif re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name):
#         item_weight = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))

#     if (item_name or item_weight or item_price or item_concentration) is not None:
#         print(item_name + " : " + str(item_weight) + " : " + item_concentration + " : " + item_price)
    
mercado_livre_url = requests.get(
    "https://lista.mercadolivre.com.br/soda-caustica")

soup = bs(mercado_livre_url.content, 'html.parser')

product_list = soup.select("li.results-item")

for item in product_list:
    item_name = item.select_one('span', class_='main-title').text
    if item.find(class_='price__decimals'):
        item_price = float(item.find(class_='price__fraction').text + \
            '.' + item.find(class_='price__decimals').text)
    else:
        item_price = float(item.find(class_='price__fraction').text)
    item_weight = 0
    item_concentration = ''
    if re.search(r'9(8|9)\%', item_name):
        item_concentration = str(re.search(r'9(8|9)\%', item_name).group(0))
    
    if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name) and re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(3) == ("G" or "g"):
        item_weight = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))/100

    elif re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name):
        item_weight = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))
    
    if re.search(r'(\d+)[x|X]', item_name):
        item_weight = float(re.search(r'(\d+)[x|X]', item_name).group(1)) * item_weight

    if (item_name or item_weight or item_price or item_concentration) is not None:
        print(item_name + " : " + str(item_weight) + " : " + item_concentration + " : " + str(item_price))

