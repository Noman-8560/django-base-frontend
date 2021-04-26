# Generated by Django 3.1.6 on 2021-04-26 20:33

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of this organization it must be same to to your organization it will be visible in many places like footer and header etc.', max_length=50)),
                ('code', models.CharField(help_text='Your code of business or lines that defines cocognito it is hero heading line text will be visible on the top section of home page.', max_length=1000)),
                ('description', models.TextField(help_text='Small description about this system or your goal, it is hero description will be visible on home page top section under hero heading.', max_length=1000)),
                ('hero_button_1_text', models.CharField(blank=True, help_text='Hero button 1', max_length=255, null=True)),
                ('hero_button_2_text', models.CharField(blank=True, help_text='Hero button 2', max_length=255, null=True)),
                ('hero_button_1_url', models.URLField(blank=True, help_text='When user clicks hero button 1 where to redirect user, please add complete url here.', null=True)),
                ('hero_button_2_url', models.URLField(blank=True, help_text='When user clicks hero button 2 where to redirect user, please add complete url here.', null=True)),
                ('hero_image', models.ImageField(blank=True, help_text='Hero Image will be visible on the right side of Hero section, please add png image with transparent sides for better display.', null=True, upload_to='website/images/hero_image/')),
                ('hero_image_display', models.BooleanField(default=False, help_text='Allow hero image to display, default is false.')),
                ('hero_buttons_display', models.BooleanField(default=False, help_text='Allow hero buttons to display, default is false.')),
                ('system_description', ckeditor.fields.RichTextField(help_text='Detailed description for cocognito, leave it blank if not needed, REMEBER: if this does not fulfills your requirements select the right most icon and add custom code, do at your own risk, try to avoid dangerous scripts that may breach your security.')),
                ('phone', models.CharField(help_text='Add support or helpline no for customer to contact you, it will be visible in footer.', max_length=18)),
                ('support_mail', models.EmailField(help_text='Add support or help email like [support@cocognito.com or help@cocognito.com] for customer to contact you, it will be visible in footer.', max_length=254)),
                ('organization_mail', models.EmailField(blank=True, help_text='Add your business email address, will be visible in footer.', max_length=254, null=True)),
                ('organization_phone', models.CharField(blank=True, help_text='Add your organization contact no, will be visible in footer.', max_length=18, null=True)),
                ('business_address', models.TextField(help_text='Add your organization or main office address, will be visible in footer.')),
                ('facebook', models.URLField(blank=True, help_text='Add complete url of your facebook account, page or group or you can leave it blank if not available,if available it will be visible in footer', null=True)),
                ('instagram', models.URLField(blank=True, help_text='Add complete url of your instagram account or you can leave it blank if not available, if available it will be visible in footer', null=True)),
                ('google', models.URLField(blank=True, help_text='Add complete url of your google account or you can leave it blank if not available, if available it will be visible in footer', null=True)),
                ('footer_organization_name', models.CharField(help_text='Please add cocognito or cocognito parent organization whom you have coyright.', max_length=50)),
                ('footer_organization_url', models.CharField(blank=True, help_text='Please add url of your parent organization or leave it blank', max_length=50, null=True)),
                ('footer_developers_name', models.CharField(blank=True, help_text='Not available now _ if you need customization for this please contact cocognito development team for this.', max_length=50, null=True)),
                ('footer_developers_url', models.CharField(blank=True, help_text='Not available now _ if you need customization for this please contact cocognito development team for this.', max_length=50, null=True)),
                ('footer_description', models.TextField(help_text='Add a small description on your footer, information about cocognito / copyright or any other details')),
                ('full_footer_display', models.BooleanField(default=True, help_text='Show complete footer')),
            ],
            options={
                'verbose_name': 'Website',
                'verbose_name_plural': 'Websites',
            },
        ),
        migrations.CreateModel(
            name='WebsiteEvents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(max_length=255)),
                ('details', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('is_current', models.BooleanField(default=False, help_text='The event is currently active')),
                ('is_active', models.BooleanField(default=True, help_text='Show this event on home page.')),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='WebsiteModules',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.PositiveIntegerField(blank=True, unique=True)),
                ('pic', models.ImageField(upload_to='project/images/modules/')),
                ('heading', models.CharField(max_length=100, unique=True)),
                ('description', ckeditor.fields.RichTextField()),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Website Module',
                'verbose_name_plural': 'Website Modules',
            },
        ),
        migrations.CreateModel(
            name='WebsiteTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Full name of a team member', max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, help_text='Image must be 200*200px and format must be jpeg, jpg or png', null=True, upload_to='website/images/team/')),
                ('description', models.TextField(help_text='Small description about this member', max_length=100)),
                ('rank', models.CharField(help_text='Member current status or rank in cocognito', max_length=50)),
                ('phone', models.CharField(default='000 000 00 00 0', max_length=18)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('facebook', models.URLField(blank=True, help_text='Complete Facebook link/url of members profile', null=True)),
                ('linkedin', models.URLField(blank=True, help_text='Complete Linkedin link/url of members profile', null=True)),
                ('is_active', models.BooleanField(default=True, help_text='Show this member on home site')),
            ],
            options={
                'verbose_name': 'member',
                'verbose_name_plural': 'Team',
            },
        ),
    ]
