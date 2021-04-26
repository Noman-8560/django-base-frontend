# Generated by Django 3.1.6 on 2021-04-13 12:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='quiz',
        ),
        migrations.AlterField(
            model_name='quiz',
            name='questions',
            field=models.ManyToManyField(to='src.application.Question'),
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.application.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='src.application.quiz')),
                ('submission_control', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='src.application.screen')),
            ],
        ),
    ]
