# Generated by Django 3.2.9 on 2021-12-29 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0010_auto_20211226_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='total_players',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='total_teams',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='quiz',
            name='total_teams_passed',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='learning_purpose',
            field=models.BooleanField(default=False, help_text='By checking Learning purpose some changes will be applied to this quiz, it will only visible for learning resource, quiz will be different from main quizzes, student can only use this quiz for learning purpose'),
        ),
    ]
