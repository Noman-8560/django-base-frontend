# Generated by Django 3.1.6 on 2021-06-28 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_auto_20210628_1831'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiovisibility',
            name='url',
        ),
        migrations.RemoveField(
            model_name='imagevisibility',
            name='url',
        ),
        migrations.AlterField(
            model_name='audiovisibility',
            name='audio',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.questionaudio'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='imagevisibility',
            name='image',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.questionimage'),
            preserve_default=False,
        ),
    ]