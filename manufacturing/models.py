from django.db import models
import os, os.path
import shutil
import datetime


class Manufacturing(models.Model):
    start_of_manufacture = models.DateTimeField()
    end_of_manufacture = models.DateTimeField()
    amount_of_soap = models.DecimalField(decimal_places=2, max_digits=4)
    expected_ph = models.DecimalField(decimal_places=2, max_digits=4, null=True ,blank=True)
    actual_ph = models.DecimalField(decimal_places=2, max_digits=4)
    oil_quality = models.CharField(max_length = 10)
    have_fragrance = models.BooleanField()
    oil_image = models.ImageField(upload_to='static/oil_images/')

    def reallocate_image(self):
        image = self.oil_image.read()

        if(self.oil_quality == 'GOOD'):
            new_path = './manufacturing/dataset/training_oil_dataset/good_oil/good_oil_' + str(len(os.listdir('./manufacturing/dataset/training_oil_dataset/good_oil/')) + 1) + '.jpg'
            shutil.move(self.oil_image.name, new_path)
            self.oil_image = new_path

        if(self.oil_quality == 'BAD'):
            new_path = './manufacturing/dataset/training_oil_dataset/bad_oil/bad_oil_' + str(len(os.listdir('./manufacturing/dataset/training_oil_dataset/bad_oil/')) + 1) + '.jpg'
            shutil.move(self.oil_image.name, new_path)
            self.oil_image = new_path

        if(self.oil_quality == 'MEDIUM'):
            new_path = './manufacturing/dataset/training_oil_dataset/medium_oil/medium_oil_' + str(len(os.listdir('./manufacturing/dataset/training_oil_dataset/medium_oil/')) + 1) + '.jpg'
            shutil.move(self.oil_image.name, new_path)
            self.oil_image = new_path

        if(self.oil_quality == 'NO OIL'):
            new_path = './manufacturing/dataset/training_oil_dataset/no_oil/no_oil_' + str(len(os.listdir('./manufacturing/dataset/training_oil_dataset/no_oil/')) + 1) + '.jpg'
            shutil.move(self.oil_image.name, new_path)
            self.oil_image = new_path

        super(Manufacturing, self).save(force_update=True)


    def save(self, *args, **kwargs):
        super(Manufacturing, self).save(*args, **kwargs)
        self.reallocate_image()
