# Generated by Django 3.2.12 on 2022-03-15 15:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0023_auto_20220130_2143'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningresourceattempts',
            name='choice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.questionchoice'),
            preserve_default=False,
        ),
    ]
