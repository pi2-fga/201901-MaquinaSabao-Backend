from django.shortcuts import render
import requests
import re
from bs4 import BeautifulSoup as bs
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.

def cheaper_soda_americanas():
    lojas_americanas_url = requests.get("https://www.americanas.com.br/busca/soda-caustica")

    soup = bs(lojas_americanas_url.content, 'html.parser')

    product_list = soup.select("div.product-grid-item > div:nth-child(1)")

    cheaper_product = {'item_description':'','item_weight':1, 'item_concentration':'', 'item_price':100,'item_link':''}

    for item in product_list:
        item_name = item.get('name')
        item_concentration = None
        item_weight = None
        if item.select_one("div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > section:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)"):
            item_price = float(re.search(r'R\$\s*(\d{1,5}\,\d{1,2})', item.select_one("div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > section:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)").text).group(1).replace(',','.'))

        if re.search(r'9(8|9)\%', item_name):
            item_concentration = str(re.search(r'9(8|9)\%', item_name).group(0))

        if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name):
            if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(3) == ("G" or "g"):
                item_weight = float(re.search(
                    r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))/100
            else:
                item_weight = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))
            if re.search(r'(\d+)[x|X]', item_name):
                item_weight = float(re.search(r'(\d+)[x|X]', item_name).group(1)) * item_weight
        
        if item.select_one('div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')['href']:
            item_link = "https://www.americanas.com.br" + item.select_one('div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')['href']

        if (item_name and item_price and item_concentration and item_weight) and ((item_price/item_weight) < (cheaper_product['item_price']/cheaper_product['item_weight'])):
            cheaper_product['item_description'] = item_name
            cheaper_product['item_weight'] = item_weight
            cheaper_product['item_concentration'] = item_concentration
            cheaper_product['item_price'] = item_price
            cheaper_product['item_link'] = item_link

    return cheaper_product     

def cheaper_soda_ml():
    mercado_livre_url = requests.get("https://lista.mercadolivre.com.br/soda-caustica")

    soup = bs(mercado_livre_url.content, 'html.parser')

    product_list = soup.select("li.results-item")

    cheaper_product = {'item_description':'','item_weight':1, 'item_concentration':'', 'item_price':100,'item_link':''}

    for item in product_list:
        item_name = item.select_one('span', class_='main-title').text
        item_concentration = None
        item_weight = None

        if item.find(class_='price__decimals'):
            item_price = float(item.find(class_='price__fraction').text + \
                '.' + item.find(class_='price__decimals').text)
        else:
            item_price = float(item.find(class_='price__fraction').text)
        
        if re.search(r'9(8|9)\%', item_name):
            item_concentration = str(re.search(r'9(8|9)\%', item_name).group(0))
        
        if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name):
            if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(3) == ("G" or "g"):
                item_weight = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))/100
            else:
                item_weight = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))
            if re.search(r'(\d+)[x|X]', item_name):
                item_weight = float(re.search(r'(\d+)[x|X]', item_name).group(1)) * item_weight

        if item.select_one("div:nth-child(2) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)"):
            item_link = item.select_one("div:nth-child(2) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)")['href']
        
        if (item_name and item_price and item_concentration and item_weight) and ((item_price/item_weight) < (cheaper_product['item_price']/cheaper_product['item_weight'])):
            cheaper_product['item_description'] = item_name
            cheaper_product['item_weight'] = item_weight
            cheaper_product['item_concentration'] = item_concentration
            cheaper_product['item_price'] = item_price
            cheaper_product['item_link'] = item_link

    return cheaper_product 

@api_view(['GET'])
def get_cheaper_soda(request):
    cheaper_americanas = cheaper_soda_americanas()
    cheaper_ml = cheaper_soda_ml()
    if cheaper_americanas['item_description'] == '' and cheaper_ml['item_description'] == '':
        return Response(status=400)
    else:
        if (cheaper_americanas['item_price']/cheaper_americanas['item_weight']) < (cheaper_ml['item_price']/cheaper_ml['item_weight']):
            return Response(cheaper_americanas, status=200)
        else:
            return Response(cheaper_ml, status=200)




@api_view(['GET'])
def get_cheaper_alcohol_ml(request):
    mercado_livre_url = requests.get("https://lista.mercadolivre.com.br/%C3%A1lcool-l%C3%ADquido-92.8")

    soup = bs(mercado_livre_url.content, 'html.parser')

    product_list = soup.select("li.results-item")

    cheaper_product = {'item_description':'','item_volume':1, 'item_concentration':'', 'item_price':100,'item_link':''}

    for item in product_list:
        item_name = item.select_one('span', class_='main-title').text
        item_concentration = None
        item_volume = None

        if item.find(class_='price__decimals'):
            item_price = float(item.find(class_='price__fraction').text + \
                '.' + item.find(class_='price__decimals').text)
        else:
            item_price = float(item.find(class_='price__fraction').text)
        
        if re.search(r'(92\,?\.?8?)', item_name):
            item_concentration = str(re.search(r'(92\,?\.?8?)', item_name).group(0))
        
        if re.search(r'(\d{1,4})\s?((Litros)|(LITROS)|l|L)\s', item_name):
            item_volume = float(re.search(r'(\d{1,4})\s?((Litros)|(LITROS)|l|L)\s', item_name).group(1))

        if item.select_one("div:nth-child(2) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)"):
            item_link = item.select_one("div:nth-child(2) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)")['href']
        
        if (item_name and item_price and item_concentration and item_volume) and ((item_price/item_volume) < (cheaper_product['item_price']/cheaper_product['item_volume'])):
            cheaper_product['item_description'] = item_name
            cheaper_product['item_volume'] = item_volume
            cheaper_product['item_concentration'] = item_concentration
            cheaper_product['item_price'] = item_price
            cheaper_product['item_link'] = item_link

    if cheaper_product['item_description'] == '':
        return Response(status=400)
    else:
        return Response(cheaper_product, status=200) 