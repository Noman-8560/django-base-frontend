# Generated by Django 3.1.6 on 2021-06-28 15:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev', '0011_auto_20210628_1831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developmentproject',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 26, 20, 55, 21, 502566)),
        ),
        migrations.AlterField(
            model_name='developmentproject',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 28, 20, 55, 21, 502566)),
        ),
    ]
