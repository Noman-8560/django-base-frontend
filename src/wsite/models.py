from django.db import models
from django_resized import ResizedImageField


class Content(models.Model):
    hero_pre_heading = models.CharField(max_length=1000, default="Play, Learn and Grow")
    hero_heading = models.CharField(max_length=1000, default="Lets Learn Together")
    hero_paragraph_1 = models.TextField(
        default="Human beings are social animals and we have been successful in becoming the most dominant "
                "species, by way of our team effort. Great news is we thrive when we work as a team. "
                "But then why should learning activity be a isolated and single person effort. At CoCognito, "
                "we believe learning need not be a single person effort. Rather it should be a social activity."
    )
    hero_paragraph_2 = models.TextField(
        default="That way it is more engaging, lasting and should be say, more FUN :-) So we have built quizzes "
                "here on variety of subjects that you can practice together with your friend(s). Remember, idea "
                "here is not to compete. But to work together to problem solve a situation. You share ideas, "
                "discuss them, suggest point of views, take suggestions and finally make a decision. Sounds fun, "
                "rite?"
    )
    hero_end_line = models.CharField(max_length=1000, default="Come lets CoCognito !")

    class Meta:
        verbose_name_plural = "Content"

    def __str__(self):
        return self.hero_heading


class Team(models.Model):
    name = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    image = ResizedImageField(
        upload_to='website/images/team/', null=True, blank=True, size=[300, 300], quality=75, force_format='PNG',
        help_text='size of logo must be 300*300 and format must be png image file', crop=['middle', 'center']
    )

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Team"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    TESTIMONIAL_TYPE = (
        ('p', 'Parent'),
        ('s', 'Student'),
        ('m', 'Moderator'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField(default="Description not provided yet.")
    testimonial_type = models.CharField(max_length=1, choices=TESTIMONIAL_TYPE)
    image = ResizedImageField(
        upload_to='website/images/testimonial/', null=True, blank=True, size=[300, 300], quality=75,
        force_format='PNG',
        help_text='size of logo must be 300*300 and format must be png image file', crop=['middle', 'center']
    )

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name


class Partner(models.Model):
    name = models.CharField(max_length=255)
    image = ResizedImageField(
        upload_to='website/images/partner/', null=True, blank=True, size=[195, 65], quality=75, force_format='PNG',
        help_text='size of logo must be 195*65 and format must be png image file', crop=['middle', 'center']
    )

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Partners"

    def __str__(self):
        return self.name
