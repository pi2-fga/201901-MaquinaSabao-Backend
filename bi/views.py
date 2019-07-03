from django.shortcuts import render
import requests
import re
from bs4 import BeautifulSoup as bs
from rest_framework.decorators import api_view
from rest_framework.response import Response

def cheaper_soda_americanas():
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    lojas_americanas_url = requests.get("https://www.americanas.com.br/busca/soda-caustica", allow_redirects=False, headers=headers)

    soup = bs(lojas_americanas_url.content, 'html.parser')

    product_list = soup.select("div.product-grid-item > div:nth-child(1)")

    cheaper_product = {'item_description': '', 'item_volume': 1,
                       'item_concentration': '', 'item_price': 100, 'item_link': '', 'item_img': ''}

    for item in product_list:
        item_name = item.get('name')
        item_concentration = None
        item_volume = None
        if item.select_one("div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > section:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)"):
            item_price = float(re.search(r'R\$\s*(\d{1,5}\,\d{1,2})', item.select_one("div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1) > section:nth-child(1) > div:nth-child(3) > div:nth-child(2) > div:nth-child(3) > span:nth-child(1)").text).group(1).replace(',','.'))

        if re.search(r'9(8|9)\%', item_name):
            item_concentration = str(re.search(r'9(8|9)\%', item_name).group(0))

        if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name):
            if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(3) == ("G" or "g"):
                item_volume = float(re.search(
                    r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))/100
            else:
                item_volume = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))
            if re.search(r'(\d+)[x|X]', item_name):
                item_volume = float(re.search(r'(\d+)[x|X]', item_name).group(1)) * item_volume

        if item.select_one('div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')['href']:
            item_link = "https://www.americanas.com.br" + item.select_one('div.product-grid-item > div:nth-child(1) > div:nth-child(2) > a:nth-child(1)')['href']

        if (item_name and item_price and item_concentration and item_volume) and ((item_price/item_volume) < (cheaper_product['item_price']/cheaper_product['item_volume'])):
            cheaper_product['item_description'] = item_name
            cheaper_product['item_volume'] = item_volume
            cheaper_product['item_concentration'] = item_concentration
            cheaper_product['item_price'] = item_price
            cheaper_product['item_link'] = item_link

            img_url = requests.get(item_link, headers=headers)
            soup_img = bs(img_url.content, 'html.parser')
            if soup_img.select_one(".image-gallery-image > img:nth-child(1)"):
                cheaper_product['item_img'] = soup_img.select_one(
                    ".image-gallery-image > img:nth-child(1)")['src']

    return cheaper_product

def cheaper_soda_ml():
    mercado_livre_url = requests.get("https://lista.mercadolivre.com.br/soda-caustica")

    soup = bs(mercado_livre_url.content, 'html.parser')

    product_list = soup.select("li.results-item")

    cheaper_product = {'item_description': '', 'item_volume': 1,
                       'item_concentration': '', 'item_price': 100, 'item_link': '', 'item_img': ''}

    for item in product_list:
        item_name = item.select_one('span', class_='main-title').text
        item_concentration = None
        item_volume = None

        if item.find(class_='price__decimals'):
            item_price = float(item.find(class_='price__fraction').text + \
                '.' + item.find(class_='price__decimals').text)
        else:
            item_price = float(item.find(class_='price__fraction').text)

        if re.search(r'9(8|9)\%', item_name):
            item_concentration = str(re.search(r'9(8|9)\%', item_name).group(0))

        if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name):
            if re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(3) == ("G" or "g"):
                item_volume = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))/100
            else:
                item_volume = float(re.search(r'((\d{1,3})\s*([Kk][Gg][Ss]?|[Gg]))', item_name).group(2))
            if re.search(r'(\d+)[x|X]', item_name):
                item_volume = float(re.search(r'(\d+)[x|X]', item_name).group(1)) * item_volume

        if item.select_one("div:nth-child(2) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)"):
            item_link = item.select_one("div:nth-child(2) > div:nth-child(1) > h2:nth-child(1) > a:nth-child(1)")['href']

        if (item_name and item_price and item_concentration and item_volume) and ((item_price/item_volume) < (cheaper_product['item_price']/cheaper_product['item_volume'])):
            cheaper_product['item_description'] = item_name
            cheaper_product['item_volume'] = item_volume
            cheaper_product['item_concentration'] = item_concentration
            cheaper_product['item_price'] = item_price
            cheaper_product['item_link'] = item_link

            img_url = requests.get(item_link)
            soup_img = bs(img_url.content, 'html.parser')
            if soup_img.select_one("label.gallery__thumbnail:nth-child(1) > img"):
                cheaper_product['item_img'] = soup_img.select_one(
                    "label.gallery__thumbnail:nth-child(1) > img")['src']


    return cheaper_product

@api_view(['GET'])
def get_cheaper_soda(request):
    cheaper_ml = cheaper_soda_ml()
    if cheaper_ml['item_description'] == '':
        return Response(status=400)
    else:
        return Response(cheaper_ml, status=200)




@api_view(['GET'])
def get_cheaper_alcohol_ml(request):
    mercado_livre_url = requests.get("https://lista.mercadolivre.com.br/%C3%A1lcool-l%C3%ADquido-92.8")

    soup = bs(mercado_livre_url.content, 'html.parser')

    product_list = soup.select("li.results-item")

    cheaper_product = {'item_description': '', 'item_volume': 1,
                       'item_concentration': '', 'item_price': 100, 'item_link': '', 'item_img': ''}

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

            img_url = requests.get(item_link)
            soup_img = bs(img_url.content, 'html.parser')
            if soup_img.select_one(".gallery-trigger"):
                cheaper_product['item_img'] = soup_img.select_one(".gallery-trigger")['href']

    if cheaper_product['item_description'] == '':
        return Response(status=400)
    else:
        return Response(cheaper_product, status=200)
