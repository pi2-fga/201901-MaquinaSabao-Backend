from django.db import models
import os, os.path

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


    def save(self, *args, **kwargs):
        super(Manufacturing, self).save(*args, **kwargs)
        self.reallocate_image()