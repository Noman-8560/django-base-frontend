# Generated by Django 3.1.6 on 2021-05-20 03:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dev', '0006_auto_20210429_0218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='developmentproject',
            name='last_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 17, 8, 48, 16, 642265)),
        ),
        migrations.AlterField(
            model_name='developmentproject',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 5, 20, 8, 48, 16, 642265)),
        ),
    ]
