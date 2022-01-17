# Generated by Django 3.2.9 on 2022-01-14 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0020_quiz_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'managed': True, 'ordering': ['-created_at'], 'verbose_name_plural': 'Questions'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Quizzes'},
        ),
        migrations.AlterField(
            model_name='quiz',
            name='description',
            field=models.TextField(default='Description not provided yet.', help_text='Pleases add a description less than 120 words'),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='end_time',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='start_time',
            field=models.DateTimeField(blank=True),
        ),
    ]