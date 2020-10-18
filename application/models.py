from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    statement = models.TextField(null=False, blank=False)
    choices = models.ManyToManyField('Choice', blank=False, related_name='choices+')
    quiz = models.ManyToManyField('Quiz', blank=True, related_name='quiz')

    def __str__(self):
        return str(self.statement)

    def __unicode__(self):
        return self.statement

    class Meta:
        managed = True
        db_table = 'Questions'
        verbose_name_plural = 'Questions'


class Choice(models.Model):
    text = models.TextField(null=False, blank=False)

    def __str__(self):
        return str(self.text)

    def __unicode__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Choices'


class Subject(models.Model):
    title = models.CharField(max_length=50, null=False, blank=False)

    def __unicode__(self):
        return self.title


class Attempt(models.Model):
    question = models.ForeignKey('Question', null=False, blank=False, related_name='question-attempt+',
                                 on_delete=models.DO_NOTHING)
    user = models.ForeignKey('auth.User', null=False, blank=False, related_name='attempt-by+',
                             on_delete=models.CASCADE)


class Team(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    quiz = models.ForeignKey('Quiz', on_delete=models.DO_NOTHING, related_name='participating-in+')
    participants = models.ManyToManyField('auth.User', blank=True, related_name='participants+')


class Quiz(models.Model):
    questions = models.ManyToManyField('Question', blank=True, related_name='questions+')
    teams = models.ManyToManyField('Team', blank=True, related_name='participating-teams+')
