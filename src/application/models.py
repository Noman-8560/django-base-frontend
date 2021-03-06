from django.core.exceptions import ValidationError
from django.db import models
from django_resized import ResizedImageField

from cocognite import settings
from ckeditor.fields import RichTextField

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from src.accounts.models import StudentProfile, User


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
    is_verified_by_child = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['parent']

    def __str__(self):
        return self.parent.username


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
    name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Make sure to use the name as 'Screen 1' - 'Screen 2' and 'Screen 3'"
    )

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


class Topic(models.Model):
    title = models.CharField(max_length=50, unique=True, null=False, blank=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['subject', '-created_on']
        verbose_name_plural = 'Topics'


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


class StudentGrade(models.Model):
    name = models.CharField(max_length=255, default="Not Provided")
    description = models.TextField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Student Grades"

    def __str__(self):
        return self.name


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

    grade = models.ForeignKey(StudentGrade, on_delete=models.SET_NULL, null=True, blank=True)
    level = models.CharField(max_length=10, default='e', choices=QUESTION_LEVEL, blank=False, null=False)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    topics = models.ManyToManyField(Topic)
    question_type = models.CharField(max_length=1, choices=QUESTION_TYPE, null=False, blank=False, default='1')
    age_limit = models.PositiveIntegerField(null=False, blank=False, validators=[is_more_than_eighteen])

    # TODO: statistical calculations here --------------------------------------------------------------------
    total_times_used_in_quizzes = models.PositiveIntegerField(default=0)
    total_times_attempted_in_quizzes = models.PositiveIntegerField(default=0)
    total_times_correct_in_quizzes = models.PositiveIntegerField(default=0)

    total_times_used_in_learning = models.PositiveIntegerField(default=0)
    total_times_attempted_in_learning = models.PositiveIntegerField(default=0)
    total_times_correct_in_learning = models.PositiveIntegerField(default=0)
    # --------------------------------------------------------------------------------------------------------

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    submission_control = models.ForeignKey('Screen', blank=True, null=True, on_delete=models.SET_NULL,
                                           related_name='submitted_by')
    choices_control = models.ForeignKey('Screen', blank=True, null=True, on_delete=models.SET_NULL,
                                        related_name='select_choices')

    class Meta:
        managed = True
        verbose_name_plural = 'Questions'
        ordering = ['-created_at']

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        self.choices_control = Screen.objects.first()
        self.submission_control = self.choices_control
        super().save(*args, **kwargs)

    def get_choices(self):
        return self.questionchoice_set.all()

    def get_correct_choice(self):
        return self.questionchoice_set.filter(is_correct=True)

    def get_statement(self):
        question_statements = QuestionStatement.objects.filter(question=self)
        if question_statements:
            return question_statements.first()
        else:
            return "Statement not available"

    def calculate_difficulty(self):
        _cal = (self.total_quizzes/self.total_correct_quizzes)*100
        if _cal >= 80:
            self.level = 'e'
        elif 40 <= _cal < 80:
            self.level = 'n'
        else:
            self.level = 'h'
        self.save()


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

    learning_purpose = models.BooleanField(
        default=False,
        help_text='By checking Learning purpose some changes will be applied to this quiz, it will only visible for '
                  'learning resource, quiz will be different from main quizzes, student can only use this quiz for '
                  'learning purpose'
    )
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(default="Description not provided yet.",
                                   help_text="Pleases add a description less than 120 words")
    thumbnail = ResizedImageField(
        upload_to='images/profiles/', null=True, blank=True, size=[400, 300], quality=75, force_format='PNG',
        help_text='size of logo must be 500*500 and format must be png image file', crop=['middle', 'center']
    )
    age_limit = models.PositiveIntegerField(
        null=False, blank=False, validators=[is_more_than_eighteen],
        help_text="Age must be greater then 5 and less than 18"
    )
    subjects = models.ManyToManyField(Subject, blank=True)
    grade = models.ForeignKey(StudentGrade, on_delete=models.SET_NULL, null=True, blank=True)
    players = models.CharField(
        max_length=1, null=False, blank=False, choices=NO_OF_PLAYERS, default='1',
        help_text="Select no of players for this quiz"
    )
    questions = models.ManyToManyField(Question, through="QuizQuestion")
    topics = models.ManyToManyField(Topic)
    submission_control = models.ForeignKey(Screen, null=True, blank=True, on_delete=models.SET_NULL)

    start_time = models.DateTimeField(null=False, blank=True)
    end_time = models.DateTimeField(null=False, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    visible_on_home = models.BooleanField(default=False, help_text="Whether this quiz will be visible on website or not")

    # TODO: statistical calculations here --------------------------------------------------------------------
    total_enrolled_teams = models.PositiveIntegerField(default=0)
    total_enrolled_students = models.PositiveIntegerField(default=0)
    total_passed_student = models.PositiveIntegerField(default=0)
    total_attempted_students = models.PositiveIntegerField(default=0)
    # --------------------------------------------------------------------------------------------------------

    class Meta:
        verbose_name_plural = 'Quizzes'
        ordering = ['-id']

    def __str__(self):
        return self.title

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
    submission_control = models.ForeignKey(Screen, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.quiz.title

    def save(self, *args, **kwargs):
        screens = Screen.objects.all()
        if not screens:
            screen = Screen.objects.create(no=1, name='Screen 1')
            self.submission_control = screen
        else:
            self.submission_control = screens.first()
        super().save(*args, **kwargs)


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


class Team(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    quiz = models.ForeignKey('Quiz', on_delete=models.DO_NOTHING, related_name='participating-in+')
    participants = models.ManyToManyField('accounts.User', blank=True, related_name='participants+')

    zoom_meeting_id = models.CharField(max_length=255, blank=True, null=True)
    zoom_start_url = models.TextField(blank=True, null=True)
    zoom_join_url = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

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


class QuizMisc(models.Model):
    question = models.ForeignKey('Question', null=False, blank=False, related_name='question-attempt+',
                                 on_delete=models.DO_NOTHING)
    user = models.ForeignKey('accounts.User', null=False, blank=False, related_name='attempt-by+',
                             on_delete=models.CASCADE)
    quiz = models.ForeignKey('Quiz', null=False, blank=False, on_delete=models.CASCADE)
    choice = models.ForeignKey('QuestionChoice', null=False, blank=False, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Quiz Misc"
        verbose_name_plural = "Quiz Miscs"


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
    choice = models.ForeignKey('QuestionChoice', models.CASCADE)
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile_on_user(sender, instance, created, **kwargs):
    if created:
        user = User.objects.get(pk=instance.id)
        if user.is_student:
            profile = StudentProfile(user=user)
            profile.save()
