# Generated by Django 2.2 on 2019-06-13 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Manufacturing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_of_manufacture', models.DateTimeField()),
                ('end_of_manufacture', models.DateTimeField()),
                ('amount_of_soap', models.DecimalField(decimal_places=2, max_digits=4)),
                ('expected_ph', models.DecimalField(decimal_places=2, max_digits=4)),
                ('actual_ph', models.DecimalField(decimal_places=2, max_digits=4)),
                ('oil_quality', models.CharField(max_length=10)),
                ('have_fragrance', models.BooleanField()),
                ('oil_image', models.ImageField(upload_to='static/oil_images/')),
                ('period', models.IntegerField(blank=True, null=True)),
                ('internet_soap_price', models.DecimalField(decimal_places=8, max_digits=9)),
                ('internet_soda_price', models.DecimalField(decimal_places=8, max_digits=9)),
                ('internet_alcohol_price', models.DecimalField(decimal_places=8, max_digits=9)),
            ],
        ),
    ]
