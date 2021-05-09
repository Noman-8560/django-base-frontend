# Generated by Django 3.1.6 on 2021-04-28 20:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatementVisibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.screen')),
                ('statement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.questionstatement')),
            ],
            options={
                'verbose_name': 'Statement Visibility',
                'verbose_name_plural': 'Statements Visibility',
            },
        ),
        migrations.CreateModel(
            name='ChoiceVisibility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.questionchoice')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.screen')),
            ],
            options={
                'verbose_name': 'choice Visibility',
                'verbose_name_plural': 'Choices Visibility',
            },
        ),
    ]