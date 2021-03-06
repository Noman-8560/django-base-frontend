# Generated by Django 3.2.9 on 2022-01-22 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0021_auto_20220114_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='total_times_attempted_in_learning',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='question',
            name='total_times_attempted_in_quizzes',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
