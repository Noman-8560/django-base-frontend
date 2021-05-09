# Generated by Django 3.1.6 on 2021-04-28 21:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_auto_20210429_0159'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choicevisibility',
            name='quiz',
        ),
        migrations.RemoveField(
            model_name='statementvisibility',
            name='quiz',
        ),
        migrations.AddField(
            model_name='choicevisibility',
            name='quiz_question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.quizquestion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='statementvisibility',
            name='quiz_question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='application.quizquestion'),
            preserve_default=False,
        ),
    ]