from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, related_name='user+')
    created_on = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True, default=timezone.now())
    guardian = models.ForeignKey('Guardian', on_delete=models.DO_NOTHING, related_name='guardian+')

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def __unicode__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    class Meta:
        managed = True
        verbose_name_plural = 'Students'


class Guardian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True, default=timezone.now())

    def __str__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    def __unicode__(self):
        return str(self.user.first_name) + ' ' + str(self.user.last_name)

    class Meta:
        managed = True
        verbose_name_plural = 'Guardians'


class Question(models.Model):
    statement = models.TextField(null=False, blank=False)
    options = models.ManyToManyField('Option', blank=False, related_name='choices+')
    quiz = models.ManyToManyField('Quiz', blank=True, related_name='quiz')
    subject = models.ForeignKey('Subject', blank=False, null=False, related_name='subject', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True, default=timezone.now())

    def __str__(self):
        return str(self.statement)

    def __unicode__(self):
        return self.statement

    class Meta:
        managed = True
        verbose_name_plural = 'Questions'


class Option(models.Model):
    text = models.TextField(null=False, blank=False)
    is_correct = models.BooleanField(null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True, default=timezone.now())

    def __str__(self):
        return str(self.text)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Options'


class Subject(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)
    created_on = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True, default=timezone.now())

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
    created_on = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True, default=timezone.now())

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
    created_on = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True, default=timezone.now())

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
    created_on = models.DateTimeField(auto_now_add=True, default=timezone.now())
    updated_on = models.DateTimeField(auto_now=True, default=timezone.now())

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Quizzes'
