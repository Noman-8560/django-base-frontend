# Generated by Django 2.2.4 on 2020-11-22 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20201112_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionstatement',
            name='screen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.Screen'),
        ),
    ]
