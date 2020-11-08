from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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


class Option(models.Model):
    text = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.text)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name = 'Option'
        verbose_name_plural = 'Options'


'''________________________________________________________________________________'''


class Question(models.Model):
    options = models.ManyToManyField('Option', through='QuestionOption', blank=False, related_name='choices+')
    quiz = models.ManyToManyField('Quiz', blank=True, related_name='quiz')
    submission_control = models.ForeignKey('Screen', blank=True, null=True, on_delete=models.SET_NULL,
                                           related_name='submited_by')
    choices_control = models.ForeignKey('Screen', blank=True, null=True, on_delete=models.SET_NULL,
                                        related_name='select_choices')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    image_hint_url = models.URLField(null=True, blank=True, max_length=500)
    audio_hint_url = models.URLField(null=True, blank=True, max_length=500)
    image_hint_file = models.FileField(upload_to='static/Uploads/', null=True, blank=True)
    audio_hint_file = models.FileField(upload_to='static/Uploads/', null=True, blank=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)

    def __unicode__(self):
        return self.pk

    class Meta:
        managed = True
        verbose_name_plural = 'Questions'


class QuestionStatement(models.Model):
    statement = models.CharField(max_length=1000, null=False, blank=False)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE, null=False, blank=False)
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
    image = models.ImageField(upload_to=None, height_field=200, width_field=200, null=True, blank=True)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE, null=False, blank=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.pk

    def __unicode__(self):
        return self.pk

    class Meta:
        managed = True
        verbose_name = 'Question Image'
        verbose_name_plural = 'Questions Images'


class QuestionAudio(models.Model):
    url = models.URLField(null=True, blank=True)
    audio = models.FileField(upload_to=None, null=True, blank=True)
    screen = models.ForeignKey('Screen', on_delete=models.CASCADE, null=False, blank=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.pk

    def __unicode__(self):
        return self.pk

    class Meta:
        managed = True
        verbose_name = 'Question Audio'
        verbose_name_plural = 'Questions Audios'


class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField(null=False, blank=False, default=False)

    def __str__(self):
        return str(self.question.id)

    def __unicode__(self):
        return self.option

    class Meta:
        verbose_name_plural = 'Question Options'
        verbose_name = 'Question Option'


'''________________________________________________________________________________'''


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
    is_active = models.BooleanField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Teams'


class Quiz(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False)
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
