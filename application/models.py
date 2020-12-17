from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField


class AppUpdate(models.Model):
    UPDATE_STATUS = (
        ('des', 'Designing'),
        ('dev', 'Development'),
        ('des', 'Testing'),
    )
    url = models.CharField(max_length=255, null=False, blank=False)
    desc = models.CharField(max_length=255, null=False, blank=False)
    status = models.CharField(max_length=3, null=False, blank=False, choices=UPDATE_STATUS)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.desc

    def __unicode__(self):
        return self.pk

    class Meta:
        managed = True
        verbose_name = 'Application Update'
        verbose_name_plural = 'Application Updates'


class Screen(models.Model):
    no = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"Screen_No: {str(self.no)} Screen_Name: {self.name}"

    def __unicode__(self):
        return self.no

    class Meta:
        managed = True
        verbose_name = 'Quiz Screen'
        verbose_name_plural = 'Quiz Screens'


class QuestionType(models.Model):
    no_of_players = models.PositiveIntegerField(null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.pk

    class Meta:
        managed = True
        verbose_name = 'Question Type'
        verbose_name_plural = 'Question Types'


class Subject(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Subjects'


class Article(models.Model):
    ARTICLE_TYPE = (
        ('e', 'Event'),
        ('a', 'Announcement'),
        ('o', 'Other'),
    )
    topic = models.CharField(max_length=255, null=False, blank=False)
    event = models.CharField(max_length=1, null=False, blank=False, choices=ARTICLE_TYPE)
    content = RichTextField(null=False, blank=False)

    active = models.BooleanField(default=True,
                                 help_text="ACTIVE : field is used to hide or show this post, if you will check this "
                                           "post it will be displayed in news feed else it will be hidden.")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.topic

    def __unicode__(self):
        return self.id

    class Meta:
        managed = True
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


'''________________________________________________________________________________'''


def is_more_than_eighteen(value):
    if value > 18:
        raise ValidationError('Value must be less than 18.')
    pass


class Question(models.Model):
    QUESTION_LEVEL = (
        ('e', 'Easy'),
        ('n', 'Normal'),
        ('h', 'Hard'),
    )

    quiz = models.ManyToManyField('Quiz', blank=True, related_name='quiz')
    level = models.CharField(max_length=10, default='e', choices=QUESTION_LEVEL, blank=False, null=False)
    submission_control = models.ForeignKey('Screen', blank=True, null=True, on_delete=models.SET_NULL,
                                           related_name='submitted_by')
    choices_control = models.ForeignKey('Screen', blank=True, null=True, on_delete=models.SET_NULL,
                                        related_name='select_choices')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    age_limit = models.PositiveIntegerField(null=False, blank=False, validators=[is_more_than_eighteen])
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.pk)

    def __unicode__(self):
        return self.pk

    class Meta:
        managed = True
        verbose_name_plural = 'Questions'


class QuestionStatement(models.Model):
    statement = models.TextField(null=False, blank=False,
                                 help_text='add your question statement/defination here you can add multiple statements to.')
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE, null=True, blank=True)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.statement

    def __unicode__(self):
        return self.statement

    class Meta:
        managed = True
        verbose_name = 'Question Statement'
        verbose_name_plural = 'Questions Statements'


class QuestionImage(models.Model):
    url = models.URLField(null=True, blank=True)
    image = models.ImageField(
        upload_to='images/projects/',
        null=True, blank=True,
        help_text='size of image less then 500*500 and format must be png, jpg or jpeg image file - '
    )
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE, null=False, blank=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return str(self.url)

    def __unicode__(self):
        return self.pk

    class Meta:
        managed = True
        verbose_name = 'Question Image'
        verbose_name_plural = 'Questions Images'


class QuestionAudio(models.Model):
    url = models.URLField(null=True, blank=True)
    audio = models.FileField(
        upload_to='audios/projects/',
        null=True, blank=True,
        help_text='size of audio less then 5MB and format must be mps, ogg etc'
    )
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE, null=False, blank=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return str(self.pk)

    def __unicode__(self):
        return self.pk

    class Meta:
        managed = True
        verbose_name = 'Question Audio'
        verbose_name_plural = 'Questions Audios'


class QuestionChoice(models.Model):
    text = models.CharField(max_length=255, null=False, blank=False)
    is_correct = models.BooleanField(default=False, null=False, blank=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.text)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'Question Choice'
        verbose_name_plural = 'Questions Choices'


'''________________________________________________________________________________'''


class Quiz(models.Model):
    NO_OF_PLAYERS = (
        ('2', 'Two Players'),
        ('3', 'Three Players'),
    )

    title = models.CharField(max_length=100, null=False, blank=False)
    age_limit = models.PositiveIntegerField(null=False, blank=False, validators=[is_more_than_eighteen])
    subjects = models.ManyToManyField(Subject, blank=False)
    players = models.CharField(max_length=1, null=False, blank=False, choices=NO_OF_PLAYERS, default='3')
    questions = models.ManyToManyField('Question', blank=True, related_name='questions+')
    teams = models.ManyToManyField('Team', blank=True, related_name='participating-teams+')
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Quizzes'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user+')
    guardian = models.ForeignKey('Guardian', on_delete=models.DO_NOTHING, related_name='guardian+')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def __unicode__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    class Meta:
        managed = True
        verbose_name_plural = 'Students'


class Guardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def __unicode__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    class Meta:
        managed = True
        verbose_name_plural = 'Guardians'


class Attempt(models.Model):
    question = models.ForeignKey('Question', null=False, blank=False, related_name='question-attempt+',
                                 on_delete=models.DO_NOTHING)
    user = models.ForeignKey('auth.User', null=False, blank=False, related_name='attempt-by+',
                             on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    successful = models.BooleanField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question.statement + ' attempted by ' + self.user.first_name

    def __unicode__(self):
        return self.question.statement

    class Meta:
        verbose_name_plural = 'Attempts'


class Team(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    quiz = models.ForeignKey('Quiz', on_delete=models.DO_NOTHING, related_name='participating-in+')
    participants = models.ManyToManyField('auth.User', blank=True, related_name='participants+')
    is_active = models.BooleanField(null=False, blank=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Teams'
