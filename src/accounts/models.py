from django.contrib.auth.models import AbstractUser
from django.db import models
from django_resized import ResizedImageField

from cocognite import settings
# from src.application.models import StudentGrade


class User(AbstractUser):
    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )

    is_student = models.BooleanField(default=False, help_text="This account belongs to student")
    is_moderator = models.BooleanField(default=False, help_text="This account belongs to Moderator/Teacher")
    is_parent = models.BooleanField(default=False, help_text="This account is parental")
    is_completed = models.BooleanField(default=False, help_text="Shows weather the account is associated with any type")

    profile_image = ResizedImageField(
        upload_to='images/profiles/', null=True, blank=True, size=[200, 200], quality=75, force_format='PNG',
        help_text='size of logo must be 100*100 and format must be png image file', crop=['middle', 'center']
    )
    gender = models.CharField(max_length=1, null=True, blank=True, choices=GENDER_CHOICE)
    about = models.TextField(null=True, blank=True, help_text="Tell us something interesting about yourself")
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)

    # GET USER PROFILE
    def get_student_profile(self):
        profiles = StudentProfile.objects.filter(user__pk=self.pk, user__is_student=True)
        if not profiles and self.is_student:
            return StudentProfile.objects.create(user=self)
        return profiles.first() if profiles else None


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student-profile+")

    # STUDENT ZOOM
    zoom_account = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Your official zoom account email address, if you don't have account yet please signup to zoom first"
    )
    zoom_account_verification = models.BooleanField(default=False)
    zoom_user_id = models.CharField(max_length=255, null=True, blank=True)

    # STUDENT STATISTICS
    total_quizzes = models.PositiveIntegerField(default=0)
    passed_quizzes = models.PositiveIntegerField(default=0)
    total_learning = models.PositiveIntegerField(default=0)
    passed_learning = models.PositiveIntegerField(default=0)

    # STUDENT EDUCATION
    grade = models.ForeignKey('application.StudentGrade', on_delete=models.SET_NULL, null=True, blank=True)
    school_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Students Profiles"

    def __str__(self):
        return self.user.username
