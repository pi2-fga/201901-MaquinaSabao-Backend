from django.db import models
import os, os.path
import shutil
import datetime
import requests
import re
from bs4 import BeautifulSoup as bs
from bi.views import *


class Manufacturing(models.Model):
    start_of_manufacture = models.DateTimeField()
    end_of_manufacture = models.DateTimeField()
    amount_of_soap = models.DecimalField(decimal_places=2, max_digits=4)
    actual_ph = models.DecimalField(decimal_places=2, max_digits=4)
    oil_quality = models.CharField(max_length = 10)
    have_fragrance = models.BooleanField()
    oil_image = models.ImageField(upload_to='static/oil_images/', blank=True)
    internet_soap_price = models.DecimalField(decimal_places=8, max_digits=12, blank=True)
    internet_soda_price = models.DecimalField(decimal_places=8, max_digits=12, blank=True)
    internet_alcohol_price = models.DecimalField(decimal_places=8, max_digits=12, blank=True)
    device_id = models.CharField(max_length = 100)

    def reallocate_image(self):
        image = open(self.oil_image.name, 'rb').read()

        if(self.oil_quality == 'GOOD'):
            good_folder = open('./manufacturing/dataset/training_oil_dataset/good_oil/good_oil_' + str(len(os.listdir('./manufacturing/dataset/training_oil_dataset/good_oil/'))) + '.jpg', 'wb')
            good_folder.write(image)

        if(self.oil_quality == 'BAD'):
            new_path = './manufacturing/dataset/training_oil_dataset/bad_oil/bad_oil_' + str(len(os.listdir('./manufacturing/dataset/training_oil_dataset/bad_oil/')) + 1) + '.jpg'
            shutil.move(self.oil_image.name, new_path)
            self.oil_image = new_path

        if(self.oil_quality == 'NO OIL'):
            new_path = './manufacturing/dataset/training_oil_dataset/no_oil/no_oil_' + str(len(os.listdir('./manufacturing/dataset/training_oil_dataset/no_oil/')) + 1) + '.jpg'
            shutil.move(self.oil_image.name, new_path)
            self.oil_image = new_path

    def get_soap_price(self):
        ml_url = requests.get("https://lista.mercadolivre.com.br/detergente")

        soup = bs(ml_url.content, 'html.parser')

        product_list = soup.select("li.results-item")

        cheaper_product = {'item_description': '',
                        'item_volume': 1,  'item_price': 100}

        for item in product_list:
            item_name = item.select_one(
                'h2', class_='item__title list-view-item-title').text
            item_volume = None

            if item.find(class_='price__decimals'):
                    item_price = float(item.find(class_='price__fraction').text +
                                    '.' + item.find(class_='price__decimals').text)
            else:
                item_price = float(item.find(class_='price__fraction').text)

            if re.search(r'((\d{1,4})\s*(ml|ML|Ml|Litros|litros|L|l))', item_name):
                if re.search(r'((\d{1,4})\s*(ml|ML|Ml|Litros|litros|L|l))', item_name).group(3) in ['Litros', 'litros', 'L', 'l']:
                    item_volume = float(re.search(
                        r'((\d{1,4})\s*(ml|ML|Ml|Litros|litros|L|l))', item_name).group(2))*1000
                else:
                    item_volume = float(
                        re.search(r'((\d{1,4})\s*(ml|ML|Ml|Litros|litros|L|l))', item_name).group(2))

            if (item_name and item_price and item_volume) and ((item_price/item_volume) < (cheaper_product['item_price']/cheaper_product['item_volume'])):
                cheaper_product['item_description'] = item_name
                cheaper_product['item_volume'] = item_volume
                cheaper_product['item_price'] = item_price

        return (cheaper_product['item_price'] / cheaper_product['item_volume'])

    def get_ammount_of_soda(self,soda_price):
        if self.amount_of_soap == 2:
            return (0.150 * soda_price)
        if self.amount_of_soap == 4:
            return (0.200 * soda_price)
        if self.amount_of_soap == 8:
            return (0.250 * soda_price)

    def save(self, *args, **kwargs):
        soda_price = requests.get('http://0.0.0.0:8000/get_cheaper_soda/').json()
        alcohol_price = requests.get('http://0.0.0.0:8000/get_cheaper_alcohol_ml/').json()
        self.internet_soda_price = self.get_ammount_of_soda(soda_price['item_price']/soda_price['item_volume'])
        self.internet_alcohol_price = (float(self.amount_of_soap) * 0.0625)*(alcohol_price['item_price']/alcohol_price['item_volume'])
        self.internet_soap_price = (self.get_soap_price() * float(self.amount_of_soap) * 1000.00)
        super(Manufacturing, self).save(*args, **kwargs)
        self.reallocate_image()
