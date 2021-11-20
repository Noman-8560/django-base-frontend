from django.core.exceptions import ValidationError
from django.db import models

from cocognite import settings
from src.accounts.models import User
from ckeditor.fields import RichTextField

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from django.utils.text import slugify
from notifications.signals import notify


class RelationType(models.Model):
    guardian_relation_name = models.CharField(max_length=255, unique=True)
    student_relation_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Relation Types"

    def __str__(self):
        return self.guardian_relation_name


class Relation(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="parent_user")
    child = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=False,
        related_name="child_user"
    )
    relation = models.ForeignKey(RelationType, models.SET_NULL, null=True, blank=True)
    is_verified_by_child = models.BooleanField(default=False, name='Verified by Child')

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['parent']

    def __str__(self):
        return self.parent


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
        return f"Screen {str(self.no)}"

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
    title = models.CharField(max_length=50, unique=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = 'Subject'
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
    slug = models.SlugField(unique=True, null=True, blank=True)

    active = models.BooleanField(default=True,
                                 help_text="ACTIVE : field is used to hide or show this post, if you will check this "
                                           "post it will be displayed in news feed else it will be hidden.")
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        managed = True
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    def __str__(self):
        return self.topic

    def __unicode__(self):
        return self.id

    def save(self, *args, **kwargs):
        self.slug = slugify(self.topic)
        super(Article, self).save(*args, **kwargs)


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
    QUESTION_TYPE = (
        ('1', 'Single Player'),
        ('2', 'Two Player'),
        ('3', 'Three Player'),
    )

    level = models.CharField(max_length=10, default='e', choices=QUESTION_LEVEL, blank=False, null=False)
    submission_control = models.ForeignKey('Screen', blank=True, null=True, on_delete=models.SET_NULL,
                                           related_name='submitted_by')
    choices_control = models.ForeignKey('Screen', blank=True, null=True, on_delete=models.SET_NULL,
                                        related_name='select_choices')
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPE, null=False, blank=False, default='1')
    age_limit = models.PositiveIntegerField(null=False, blank=False, validators=[is_more_than_eighteen])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.choices_control = Screen.objects.first()
        self.submission_control = self.choices_control
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
        ('1', 'Single Player'),
        ('2', 'Two Players'),
        ('3', 'Three Players'),
    )

    title = models.CharField(max_length=100, null=False, blank=False)
    age_limit = models.PositiveIntegerField(
        null=False, blank=False, validators=[is_more_than_eighteen],
        help_text="Age must be greater then 5 and less than 18"
    )
    subjects = models.ManyToManyField(Subject, blank=True)
    players = models.CharField(
        max_length=1, null=False, blank=False, choices=NO_OF_PLAYERS, default='1',
        help_text="Select no of players for this quiz"
    )
    questions = models.ManyToManyField(Question, through="QuizQuestion")
    submission_control = models.ForeignKey(Screen, null=True, blank=True, on_delete=models.SET_NULL)
    start_time = models.DateTimeField(null=False, blank=False)
    end_time = models.DateTimeField(null=False, blank=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    learning_purpose = models.BooleanField(default=False,
                                           help_text='By checking Learning purpose some changes will be applied '
                                                     'to this quiz, it will only visible for learning resource, '
                                                     'quiz will be different from main quizes, '
                                                     'student can only use this quiz for learning purpose'
                                           )

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Quizzes'

    def save(self, *args, **kwargs):
        if self.learning_purpose:
            self.players = '1'
            self.submission_control = Screen.objects.first()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        teams = Team.objects.filter(quiz=self)
        if teams:
            for team in teams:
                team.delete()

        super(Quiz, self).delete(*args, **kwargs)


class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # TODO: Please solve this problem to avoid failure when the first screen id is not 1
    submission_control = models.ForeignKey(Screen, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.quiz.title


class StatementVisibility(models.Model):
    statement = models.ForeignKey(QuestionStatement, on_delete=models.CASCADE)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    screen_1 = models.BooleanField(default=True)
    screen_2 = models.BooleanField(default=False)
    screen_3 = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Statement Visibility'
        verbose_name_plural = 'Statements Visibility'

    def __str__(self):
        return str(self.pk)


class ChoiceVisibility(models.Model):
    choice = models.ForeignKey(QuestionChoice, on_delete=models.CASCADE)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    screen_1 = models.BooleanField(default=True)
    screen_2 = models.BooleanField(default=False)
    screen_3 = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'choice Visibility'
        verbose_name_plural = 'Choices Visibility'

    def __str__(self):
        return str(self.pk)


class AudioVisibility(models.Model):
    audio = models.ForeignKey(QuestionAudio, on_delete=models.CASCADE)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    screen_1 = models.BooleanField(default=True)
    screen_2 = models.BooleanField(default=False)
    screen_3 = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Audio Visibility'
        verbose_name_plural = 'Audios Visibility'

    def __str__(self):
        return str(self.pk)


class ImageVisibility(models.Model):
    image = models.ForeignKey(QuestionImage, on_delete=models.CASCADE)
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    screen_1 = models.BooleanField(default=True)
    screen_2 = models.BooleanField(default=False)
    screen_3 = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Image Visibility'
        verbose_name_plural = 'Images Visibility'

    def __str__(self):
        return str(self.pk)


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


class Team(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    quiz = models.ForeignKey('Quiz', on_delete=models.DO_NOTHING, related_name='participating-in+')
    participants = models.ManyToManyField('accounts.User', blank=True, related_name='participants+')

    zoom_meeting_id = models.CharField(max_length=255, blank=True, null=True)
    zoom_start_url = models.TextField(blank=True, null=True)
    zoom_join_url = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(null=False, blank=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Teams'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # ZOOM_API_CALL > create meet
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # ZOOM_API_CALL > delete meeting
        super(Team, self).delete(*args, **kwargs)


class Attempt(models.Model):
    question = models.ForeignKey('Question', null=False, blank=False, related_name='question-attempt+',
                                 on_delete=models.DO_NOTHING)
    user = models.ForeignKey('accounts.User', null=False, blank=False, related_name='attempt-by+',
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', null=False, blank=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    successful = models.BooleanField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Attempts'

    def __str__(self):
        return str(self.pk)

    def __unicode__(self):
        return self.question.statement

    def save(self, *args, **kwargs):
        team = Team.objects.filter(quiz=self.quiz, participants__username=self.user.username).first()
        self.team = team
        super().save(*args, **kwargs)


class LearningResourceResult(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    total = models.PositiveIntegerField(null=False, blank=False, default=0)
    obtained = models.PositiveIntegerField(null=False, blank=False, default=0)
    attempts = models.PositiveIntegerField(null=False, blank=False, default=1)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Learning Resource Result'
        verbose_name_plural = 'Learning Resource Results'

    def __str__(self):
        return 'QUIZ: ' + str(self.quiz.pk) + ' was attempted User' + str(self.user.username)


class LearningResourceAttempts(models.Model):
    question = models.ForeignKey('Question', null=False, blank=False, related_name='question-attempt+',
                                 on_delete=models.DO_NOTHING)
    user = models.ForeignKey('accounts.User', null=False, blank=False, related_name='attempt-by+',
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', null=False, blank=False, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    successful = models.BooleanField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.question.questionstatement_set.first())

    def __unicode__(self):
        return self.question.statement

    class Meta:
        verbose_name = 'Learning Resource Attempt'
        verbose_name_plural = 'Learning Resource Attempts'


class QuizCompleted(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, null=True, blank=True)
    passed = models.PositiveIntegerField(default=0, null=False, blank=False)
    remains = models.CharField(max_length=1000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    skipped = models.PositiveIntegerField(null=False, blank=False, default=0)
    total = models.PositiveIntegerField(null=False, blank=False, default=0)
    obtained = models.PositiveIntegerField(null=False, blank=False, default=0)

    class Meta:
        verbose_name = 'Completed Quiz'
        verbose_name_plural = 'Completed Quizes'

    def __str__(self):
        return 'QUIZ: ' + str(self.quiz.pk) + ' was attempted User' + str(self.user.username)


class Profile(models.Model):
    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )
    image_height = models.PositiveIntegerField(null=True, blank=True, editable=False, default="150")
    image_width = models.PositiveIntegerField(null=True, blank=True, editable=False, default="150")

    user = models.OneToOneField(User, null=False, blank=False, on_delete=models.CASCADE)
    profile = models.ImageField(
        upload_to='images/profiles/',
        height_field='image_height', width_field='image_width',
        default='images/profiles/male-avatar.png',
        help_text="Profile picture must be less then 500px of width and height, image must be in jpg, jpeg or png.",
        verbose_name="Profile Picture",
        null=False, blank=False
    )
    is_guardian = models.BooleanField(null=False, blank=False, default=False)
    date_of_birth = models.DateField(
        null=True, blank=True,
        help_text='Date of birth format must be [yyyy/mm/dd] or [yyyy-mm-dd]'
    )
    gender = models.CharField(max_length=1, null=True, blank=True, choices=GENDER_CHOICE)
    phone = models.CharField(max_length=255, unique=True, blank=True, null=True,
                             help_text='include your phone number with your country code.')
    about = models.TextField(null=True, blank=True,
                             help_text='you can add details about yourself like your hobbies, favorite lines, code of '
                                       'life, bio or other details as well'
                             )
    address = models.TextField(blank=True, null=True)

    school_name = models.CharField(max_length=255, null=True, blank=True)
    class_name = models.CharField(max_length=255, null=True, blank=True)
    class_section = models.CharField(max_length=255, null=True, blank=True)
    school_email = models.CharField(max_length=255, null=True, blank=True)
    school_address = models.TextField(null=True, blank=True)
    zoom_account = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Your official zoom account email address, if you don't have account yet please signup to zoom first"
    )
    zoom_account_verification = models.BooleanField(null=False, blank=False, default=False)
    zoom_user_id = models.CharField(max_length=200, null=False, blank=False)

    guardian_first_name = models.CharField(max_length=255, null=True, blank=True)
    guardian_last_name = models.CharField(max_length=255, null=True, blank=True)
    guardian_email = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def save_profile_on_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.id)
        profile = Profile(user=user)
        profile.save()

        from src.zoom_api.views import create_zoom_user
        # if create_zoom_user(user=user):
        #     verb = f'Zoom profile created'
        #     description = f'Hi <b>{user}</b>, your zoom profile was created, so you can join and/or start meetings.'
        # else:
        #     verb = f'Failed to create Zoom profile'
        #     description = f'Hi <b>{user}</b>, failed to create your Zoom profile, please contact the administrators.'

        # notify.send(
        #     user,
        #     recipient=user,
        #     verb=verb,
        #     level='info',
        #     description=description
        # )
