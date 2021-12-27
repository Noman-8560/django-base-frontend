# Generated by Django 3.2.9 on 2021-12-26 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_user_profile_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='studentprofile',
            options={'verbose_name_plural': 'Students Profiles'},
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='passed_learning',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='passed_quizzes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='team_quizzes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='total_learning',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='total_quizzes',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student-profile+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_student',
            field=models.BooleanField(default=False, help_text='This account belongs to student'),
        ),
    ]