# Generated by Django 3.1.6 on 2021-06-28 13:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_audiovisibility_imagevisibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionaudio',
            name='screen',
        ),
        migrations.RemoveField(
            model_name='questionimage',
            name='screen',
        ),
    ]