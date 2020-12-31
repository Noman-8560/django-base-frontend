# Generated by Django 3.1.4 on 2020-12-31 13:36

import application.models
import ckeditor.fields
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
            name='AppUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('desc', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('des', 'Designing'), ('dev', 'Development'), ('des', 'Testing')], max_length=3)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Application Update',
                'verbose_name_plural': 'Application Updates',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=255)),
                ('event', models.CharField(choices=[('e', 'Event'), ('a', 'Announcement'), ('o', 'Other')], max_length=1)),
                ('content', ckeditor.fields.RichTextField()),
                ('active', models.BooleanField(default=True, help_text='ACTIVE : field is used to hide or show this post, if you will check this post it will be displayed in news feed else it will be hidden.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Guardian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Guardians',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('e', 'Easy'), ('n', 'Normal'), ('h', 'Hard')], default='e', max_length=10)),
                ('age_limit', models.PositiveIntegerField(validators=[application.models.is_more_than_eighteen])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Questions',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuestionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_of_players', models.PositiveIntegerField()),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Question Type',
                'verbose_name_plural': 'Question Types',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('age_limit', models.PositiveIntegerField(validators=[application.models.is_more_than_eighteen])),
                ('players', models.CharField(choices=[('2', 'Two Players'), ('3', 'Three Players')], default='3', max_length=1)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('questions', models.ManyToManyField(blank=True, related_name='_quiz_questions_+', to='application.Question')),
            ],
            options={
                'verbose_name_plural': 'Quizzes',
            },
        ),
        migrations.CreateModel(
            name='Screen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.PositiveIntegerField()),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Quiz Screen',
                'verbose_name_plural': 'Quiz Screens',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('participants', models.ManyToManyField(blank=True, related_name='_team_participants_+', to=settings.AUTH_USER_MODEL)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='participating-in+', to='application.quiz')),
            ],
            options={
                'verbose_name_plural': 'Teams',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('guardian', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='guardian+', to='application.guardian')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Students',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuizCompleted',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Completed Quiz',
                'verbose_name_plural': 'Completed Quizes',
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='subjects',
            field=models.ManyToManyField(blank=True, null=True, to='application.Subject'),
        ),
        migrations.CreateModel(
            name='QuestionStatement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField(help_text='add your question statement/defination here you can add multiple statements to.')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.question')),
                ('screen', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.screen')),
            ],
            options={
                'verbose_name': 'Question Statement',
                'verbose_name_plural': 'Questions Statements',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, help_text='size of image less then 500*500 and format must be png, jpg or jpeg image file - ', null=True, upload_to='images/projects/')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.question')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.screen')),
            ],
            options={
                'verbose_name': 'Question Image',
                'verbose_name_plural': 'Questions Images',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='QuestionChoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
                ('is_correct', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.question')),
            ],
            options={
                'verbose_name': 'Question Choice',
                'verbose_name_plural': 'Questions Choices',
            },
        ),
        migrations.CreateModel(
            name='QuestionAudio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, null=True)),
                ('audio', models.FileField(blank=True, help_text='size of audio less then 5MB and format must be mps, ogg etc', null=True, upload_to='audios/projects/')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.question')),
                ('screen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.screen')),
            ],
            options={
                'verbose_name': 'Question Audio',
                'verbose_name_plural': 'Questions Audios',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='question',
            name='choices_control',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='select_choices', to='application.screen'),
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ManyToManyField(blank=True, related_name='quiz', to='application.Quiz'),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.subject'),
        ),
        migrations.AddField(
            model_name='question',
            name='submission_control',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submitted_by', to='application.screen'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_height', models.PositiveIntegerField(blank=True, default='150', editable=False, null=True)),
                ('image_width', models.PositiveIntegerField(blank=True, default='150', editable=False, null=True)),
                ('profile', models.ImageField(default='images/profiles/male-avatar.jpg', height_field='image_height', help_text='Profile picture must be less then 500px of width and height, image must be in jpg, jpeg or png.', upload_to='images/profiles/', verbose_name='Profile Picture', width_field='image_width')),
                ('is_guardian', models.BooleanField(default=False)),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Other')], max_length=1, null=True)),
                ('phone', models.CharField(blank=True, help_text='include your phone number with your country code.', max_length=255, null=True, unique=True)),
                ('about', models.TextField(blank=True, help_text='you can add details about yourself like your hobbies, favorite lines, code of life, bio or other details as well', null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('class_name', models.CharField(blank=True, max_length=255, null=True)),
                ('class_section', models.CharField(blank=True, max_length=255, null=True)),
                ('school_email', models.CharField(blank=True, max_length=255, null=True)),
                ('school_address', models.TextField(blank=True, null=True)),
                ('guardian_first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('guardian_last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('guardian_email', models.CharField(blank=True, max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.CreateModel(
            name='LearningResourceResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.PositiveIntegerField(default=0)),
                ('obtained', models.PositiveIntegerField(default=0)),
                ('attempts', models.PositiveIntegerField(default=1)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Learning Resource Result',
                'verbose_name_plural': 'Learning Resource Results',
            },
        ),
        migrations.CreateModel(
            name='LearningResourceAttempts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('successful', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='question-attempt+', to='application.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempt-by+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Learning Resource Attempt',
                'verbose_name_plural': 'Learning Resource Attempts',
            },
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('successful', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='question-attempt+', to='application.question')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='application.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attempt-by+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Attempts',
            },
        ),
    ]
