from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'wsite/home.html'


class Error404View(TemplateView):
    template_name = 'wsite/404.html'

