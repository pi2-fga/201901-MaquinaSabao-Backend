from django.db import models
import os, os.path
import requests
import re
from bs4 import BeautifulSoup as bs
from bi.views import *

# Create your models here.
class Manufacturing(models.Model):
    date_of_manufacture = models.DateField()
    start_of_manufacture = models.TimeField()
    end_of_manufacture = models.TimeField()
    amount_of_soap = models.DecimalField(decimal_places=2, max_digits=4)
    expected_ph = models.DecimalField(decimal_places=2, max_digits=4)
    actual_ph = models.DecimalField(decimal_places=2, max_digits=4)
    oil_quality = models.CharField(max_length = 10)
    have_fragrance = models.BooleanField()
    oil_image = models.ImageField(upload_to='static/oil_images/')
    internet_soap_price = models.DecimalField(decimal_places=8, max_digits=9)
    internet_soda_price = models.DecimalField(decimal_places=8, max_digits=9)
    internet_alcohol_price = models.DecimalField(decimal_places=8, max_digits=9)

    def reallocate_image(self):
        image = open('static/oil_images/' + self.oil_image.name, 'rb').read()
        
        if(self.oil_quality == 'GOOD'):
            good_folder = open('dataset/training_oil_dataset/good_oil/good_oil_' + len(os.listdir('dataset/training_oil_dataset/good_oil/')) + '.jpg', 'wb')
            good_folder.write(image)

        if(self.oil_quality == 'BAD'):
            good_folder = open('dataset/training_oil_dataset/bad_oil/bad_oil_' + len(os.listdir('dataset/training_oil_dataset/bad_oil/')) + '.jpg', 'wb')
            good_folder.write(image)

        if(self.oil_quality == 'MEDIUM'):
            good_folder = open('dataset/training_oil_dataset/medium_oil/medium_oil_' + len(os.listdir('dataset/training_oil_dataset/medium_oil/')) + '.jpg', 'wb')
            good_folder.write(image)

    def get_soap_price(self):
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
        return (cheaper_product['item_price'] / cheaper_product['item_volume'])

    def save(self, *args, **kwargs):
        soda_price = get_cheaper_soda()
        alcohol_price = get_cheaper_alcohol_ml()
        self.internet_soda_price = soda_price['item_price']/soda_price['item_volume']
        self.internet_alcohol_price = alcohol_price['item_price']/alcohol_price['item_volume']
        self.internet_soap_price = self.get_soap_price()
        super(Manufacturing, self).save(*args, **kwargs)
        self.reallocate_image()