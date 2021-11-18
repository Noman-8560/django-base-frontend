from django.contrib.auth.models import AbstractUser
from django.db import models
from cocognite import settings


class User(AbstractUser):
    GENDER_CHOICE = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )

    is_student = models.BooleanField(default=True, help_text="This account belongs to student")
    is_moderator = models.BooleanField(default=False, help_text="This account belongs to Moderator/Teacher")
    is_parent = models.BooleanField(default=False, help_text="This account is parental")
    is_completed = models.BooleanField(default=False, help_text="Shows weather the account is associated with any type")

    profile_image = models.ImageField(
        null=True, blank=True,
        upload_to='images/profiles/', height_field='150', width_field='150',
        verbose_name="Profile Picture", help_text="Profile image must be 150*150 in size of png, jpg or jpeg"
    )
    gender = models.CharField(max_length=1, null=True, blank=True, choices=GENDER_CHOICE)
    about = models.TextField(null=True, blank=True, help_text="Tell us something interesting about yourself")
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    institute = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        self.profile_image.delete(save=True)
        super(User, self).delete(*args, **kwargs)


class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)
    zoom_account = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Your official zoom account email address, if you don't have account yet please signup to zoom first"
    )
    zoom_account_verification = models.BooleanField(null=False, blank=False, default=False)
    zoom_user_id = models.CharField(max_length=200, null=False, blank=False)
