from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Website(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    code = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=255, null=False, blank=False)

    hero_button_1_text = models.CharField(max_length=20, null=True, blank=True)
    hero_button_2_text = models.CharField(max_length=20, null=True, blank=True)

    hero_button_1_url = models.URLField(null=True, blank=True)
    hero_button_2_url = models.URLField(null=True, blank=True)

    hero_image = models.ImageField(upload_to='website/images/hero_image/', null=True, blank=True)

    hero_image_display = models.BooleanField(default=False)
    hero_buttons_display = models.BooleanField(default=False)

    phone = models.CharField(max_length=18, null=True, blank=True)
    support_mail = models.EmailField(null=True, blank=True)

    organization_mail = models.EmailField(null=True, blank=True)
    organization_phone = models.CharField(max_length=18, null=True, blank=True)
    business_address = models.TextField(null=True, blank=True, )
    facebook = models.URLField(null=True, blank=True, )
    instagram = models.URLField(null=True, blank=True)
    google = models.URLField(null=True, blank=True)

    footer_organization_name = models.CharField(max_length=50, null=False, blank=False)
    footer_organization_url = models.CharField(max_length=50, null=False, blank=False)
    footer_developers_name = models.CharField(max_length=50, null=False, blank=False)
    footer_developers_url = models.CharField(max_length=50, null=False, blank=False)
    footer_description = models.TextField(max_length=255, null=True, blank=True)

    full_footer_display = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'

    def __str__(self):
        return f'{self.name}'


class WebsiteModules(models.Model):
    sequence = models.PositiveIntegerField(null=False, blank=True, unique=True)
    pic = models.ImageField(null=False, blank=False, upload_to='project/images/modules/')
    heading = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = RichTextField(blank=False, null=False, max_length=2000)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Website Module'
        verbose_name_plural = 'Website Modules'

    def __str__(self):
        return f'{self.heading}'


class WebsiteTeam(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    image = models.ImageField(
        upload_to='website/images/team/', null=True, blank=True,
    )
    description = models.TextField(null=False, blank=False)
    rank = models.CharField(max_length=50, null=False, blank=False, unique=False)
    phone = models.PositiveIntegerField(null=False, blank=False)
    email = models.EmailField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True)
    linkedin = models.URLField(null=True, blank=True)
    is_active = models.BooleanField(default=True, blank=False, null=False)

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'Team'

    def __str__(self):
        return f'{self.name}'


class WebsiteEvents(models.Model):
    sequence = models.PositiveIntegerField(null=False, blank=False, default=0)
    title = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(max_length=255, null=False, blank=False)
    details = RichTextField(null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True)
    is_current = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(WebsiteEvents, self).save(*args, **kwargs)