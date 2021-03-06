# Generated by Django 3.2.12 on 2022-03-15 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20220102_0133'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='parent_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='school_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
