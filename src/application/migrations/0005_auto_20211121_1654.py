# Generated by Django 3.2.9 on 2021-11-21 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_relation_relationtype'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relationtype',
            options={'verbose_name_plural': 'Relation Types'},
        ),
        migrations.RenameField(
            model_name='relation',
            old_name='Verified by Child',
            new_name='is_verified_by_child',
        ),
    ]
