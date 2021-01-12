from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify


class Website(models.Model):
    name = models.CharField(
        max_length=50, null=False, blank=False,
        help_text='Name of this organization it must be same to to your organization it will be '
                  'visible in many places like footer and header etc.'
    )
    code = models.CharField(
        max_length=50, null=False, blank=False,
        help_text='Your code of business or lines that defines cocognito it is hero heading line text '
                  'will be visible on the top section of home page.'
    )
    description = models.TextField(
        help_text='Small description about this system or your goal, it is hero description will be visible on '
                  'home page top section under hero heading.'
    )

    hero_button_1_text = models.CharField(max_length=20, null=True, blank=True, help_text='Hero button 1')
    hero_button_2_text = models.CharField(max_length=20, null=True, blank=True, help_text='Hero button 2')

    hero_button_1_url = models.URLField(
        null=True, blank=True,
        help_text='When user clicks hero button 1 where to redirect user, please add complete url here.'
    )
    hero_button_2_url = models.URLField(
        null=True, blank=True,
        help_text='When user clicks hero button 2 where to redirect user, please add complete url here.'
    )

    hero_image = models.ImageField(
        upload_to='website/images/hero_image/', null=True, blank=True,
        help_text='Hero Image will be visible on the right side of Hero section, please add png image with transparent '
                  'sides for better display.'
    )

    hero_image_display = models.BooleanField(
        default=False, help_text='Allow hero image to display, default is false.'
    )
    hero_buttons_display = models.BooleanField(
        default=False, help_text='Allow hero buttons to display, default is false.'
    )

    system_description = RichTextField(
        help_text='Detailed description for cocognito, leave it blank if not needed, REMEBER: if this does not '
                  'fulfills your requirements select the right most icon and add custom code, do at your own risk, '
                  'try to avoid dangerous scripts that may breach your security.'
    )

    phone = models.CharField(
        max_length=18, null=False, blank=False,
        help_text='Add support or helpline no for customer to contact you, it will be visible in footer.'

    )

    support_mail = models.EmailField(
        null=False, blank=False,
        help_text='Add support or help email like [support@cocognito.com or help@cocognito.com] '
                  'for customer to contact you, it will be visible in footer.'
    )

    organization_mail = models.EmailField(
        null=True, blank=True, help_text='Add your business email address, will be visible in footer.'
    )
    organization_phone = models.CharField(
        max_length=18, null=True, blank=True,
        help_text='Add your organization contact no, will be visible in footer.'
    )
    business_address = models.TextField(
        help_text='Add your organization or main office address, will be visible in footer.'
    )
    facebook = models.URLField(
        null=True, blank=True,
        help_text='Add complete url of your facebook account, page or group or you can leave it blank if not available,'
                  'if available it will be visible in footer'
    )
    instagram = models.URLField(
        null=True, blank=True,
        help_text='Add complete url of your instagram account or you can leave it blank if not available, '
                  'if available it will be visible in footer'
    )
    google = models.URLField(
        null=True, blank=True,
        help_text='Add complete url of your google account or you can leave it blank if not available, '
                  'if available it will be visible in footer'
    )

    footer_organization_name = models.CharField(
        max_length=50, null=False, blank=False,
        help_text='Please add cocognito or cocognito parent organization whom you have coyright.'
    )
    footer_organization_url = models.CharField(
        max_length=50, null=True, blank=True,
        help_text='Please add url of your parent organization or leave it blank'
    )
    footer_developers_name = models.CharField(
        max_length=50, null=True, blank=True,
        help_text='Not available now _ if you need customization '
                  'for this please contact cocognito development team for this.'
    )
    footer_developers_url = models.CharField(
        max_length=50, null=True, blank=True,
        help_text='Not available now _ if you need customization '
                  'for this please contact cocognito development team for this.'
    )
    footer_description = models.TextField(
        help_text='Add a small description on your footer, information about '
                  'cocognito / copyright or any other details'
    )

    full_footer_display = models.BooleanField(default=True, null=False, blank=False, help_text='Show complete footer')

    class Meta:
        verbose_name = 'Website'
        verbose_name_plural = 'Websites'

    def __str__(self):
        return f'{self.name}'


class WebsiteModules(models.Model):
    sequence = models.PositiveIntegerField(null=False, blank=True, unique=True)
    pic = models.ImageField(null=False, blank=False, upload_to='project/images/modules/')
    heading = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = RichTextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Website Module'
        verbose_name_plural = 'Website Modules'

    def __str__(self):
        return f'{self.heading}'


class WebsiteTeam(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True, help_text='Full name of a team member')
    image = models.ImageField(
        upload_to='website/images/team/', null=True, blank=True,
        help_text='Image must be 200*200px and format must be jpeg, jpg or png'
    )
    description = models.TextField(
        max_length=100, null=False, blank=False,
        help_text='Small description about this member'
    )
    rank = models.CharField(
        max_length=50, null=False, blank=False, unique=False,
        help_text='Member current status or rank in cocognito'
    )
    phone = models.CharField(max_length=18, null=False, blank=False, default='000 000 00 00 0')
    email = models.EmailField(null=True, blank=True)
    facebook = models.URLField(null=True, blank=True, help_text='Complete Facebook link/url of members profile')
    linkedin = models.URLField(null=True, blank=True, help_text='Complete Linkedin link/url of members profile')
    is_active = models.BooleanField(default=True, blank=False, null=False, help_text='Show this member on home site')

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
    is_current = models.BooleanField(default=False, help_text='The event is currently active')
    is_active = models.BooleanField(default=True, help_text='Show this event on home page.')

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(WebsiteEvents, self).save(*args, **kwargs)
