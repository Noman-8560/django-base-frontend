# Generated by Django 3.1.6 on 2021-04-26 20:34

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DevelopmentDiscussion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(choices=[('1', 'Application Idea and Research'), ('2', 'Application Design UI/UX'), ('3', 'Business Logic'), ('4', 'Bugs Issues Errors and Other problems'), ('5', 'Missing requirements and fixes'), ('6', 'Security Vulnerabilities'), ('0', 'Undefined')], help_text="Select Your discussion category if you didn't find select undefined", max_length=1)),
                ('description', models.TextField(help_text='Have something in mind? lets start to write')),
                ('is_answered', models.BooleanField(default=False)),
                ('is_satisfied', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('started_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='QUESTION_BY', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Discussion',
                'verbose_name_plural': 'Discussion Board',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentFeedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('status', models.CharField(default='1', max_length=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Client Feedback',
                'verbose_name_plural': 'Client Feedback',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentIteration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='dev/images/iterations/')),
                ('description', models.TextField(blank=True, null=True)),
                ('is_current', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Development Iteration',
                'verbose_name_plural': 'Development Iterations',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=100)),
                ('tag_line', models.CharField(default='_tag_line_not_defined_until_now_', max_length=255)),
                ('version', models.CharField(default='v0.0.1 - alpha', max_length=100)),
                ('start_date', models.DateTimeField(default=datetime.datetime(2021, 4, 27, 1, 34, 33, 321402))),
                ('last_date', models.DateTimeField(default=datetime.datetime(2021, 5, 25, 1, 34, 33, 321402))),
                ('description', models.TextField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='dev/images/project/')),
            ],
            options={
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='DevelopmentDiscussionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', ckeditor.fields.RichTextField()),
                ('is_active', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('answer_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ANSWERED_BY', to=settings.AUTH_USER_MODEL)),
                ('discussion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dev.developmentdiscussion')),
            ],
            options={
                'verbose_name': 'Discussion Answer',
                'verbose_name_plural': 'Discussion Answers',
            },
        ),
    ]