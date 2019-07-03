# Generated by Django 2.2 on 2019-06-28 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manufacturing',
            name='expected_ph',
        ),
        migrations.RemoveField(
            model_name='manufacturing',
            name='period',
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='internet_alcohol_price',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12),
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='internet_soap_price',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12),
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='internet_soda_price',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=12),
        ),
        migrations.AlterField(
            model_name='manufacturing',
            name='oil_image',
            field=models.ImageField(blank=True, upload_to='static/oil_images/'),
        ),
    ]