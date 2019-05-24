from django.db import models

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
    oil_image = models.ImageField() 