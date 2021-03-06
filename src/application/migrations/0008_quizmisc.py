# Generated by Django 3.2.9 on 2021-12-13 20:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('application', '0007_auto_20211122_1402'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizMisc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='question-attempt+', to='application.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.team')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempt-by+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Quiz Misc',
                'verbose_name_plural': 'Quiz Miscs',
            },
        ),
    ]
