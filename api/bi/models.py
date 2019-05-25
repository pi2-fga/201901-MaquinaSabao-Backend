from django.db import models
import requests
import re
from bs4 import BeautifulSoup as bs

# Create your models here.

class Product(models.Model):
    class Meta:
        abstract = True

    price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_lenght=150)
    concentration = models.CharField(max_lenght=5)
    link = models.CharField(max_lenght=150)


class SodiumHydroxide(Product):
    weight = models.DecimalField(max_digits=3, decimal_places=3)

    def __init__(self, price, description, concentration, link, weight):
        self.price = price
        self.description = description
        self.concentration = concentration
        self.link = link
        self.weight = weight

    def fill_products_list_americanas(self):
        lojas_americanas_url = requests.get("https://www.americanas.com.br/busca/soda-caustica")

        soup = bs(lojas_americanas_url.content, 'html.parser')

        product_list = soup.select("div.product-grid-item > div:nth-child(1)")
        
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

            if item_name and item_price and item_concentration and item_weight:
                SodiumHydroxide(item_price, item_name, item_concentration, item_link, item_weight)
      
    def fill_products_list_ml(self):
        mercado_livre_url = requests.get("https://lista.mercadolivre.com.br/soda-caustica")

        soup = bs(mercado_livre_url.content, 'html.parser')

        product_list = soup.select("li.results-item")

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
           
            if item_name and item_price and item_concentration and item_weight:
                SodiumHydroxide(item_price, item_name, item_concentration, item_link, item_weight)
      
    
class Alcohol(Product):
    volume = models.DecimalField(max_digits=3, decimal_places=2)

    
