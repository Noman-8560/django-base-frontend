from django.forms import ModelForm
from  .models import Website


class WebsiteForm(ModelForm):
    class Meta:
        model = Website
        fields = '__all__'
