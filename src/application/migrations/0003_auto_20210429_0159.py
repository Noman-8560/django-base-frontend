# Generated by Django 3.1.6 on 2021-04-28 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0002_choicevisibility_statementvisibility'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choicevisibility',
            name='screen',
        ),
        migrations.RemoveField(
            model_name='statementvisibility',
            name='screen',
        ),
        migrations.AddField(
            model_name='choicevisibility',
            name='screen_1',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='choicevisibility',
            name='screen_2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='choicevisibility',
            name='screen_3',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statementvisibility',
            name='screen_1',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='statementvisibility',
            name='screen_2',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='statementvisibility',
            name='screen_3',
            field=models.BooleanField(default=False),
        ),
    ]
