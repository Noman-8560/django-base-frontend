# Generated by Django 3.2.9 on 2021-11-22 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_user_institute'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, help_text='Profile image must be 150*150 in size of png, jpg or jpeg', null=True, upload_to='images/profiles/', verbose_name='Profile Picture'),
        ),
    ]
