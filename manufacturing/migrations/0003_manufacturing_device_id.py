# Generated by Django 2.2.2 on 2019-07-03 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturing', '0002_auto_20190628_1421'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufacturing',
            name='device_id',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]