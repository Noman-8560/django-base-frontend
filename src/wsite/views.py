from django.views.generic import TemplateView

from src.application.models import Quiz


class HomeView(TemplateView):
    template_name = 'wsite/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['quizzes'] = Quiz.objects.filter(visible_on_home=True, learning_purpose=False)
        context['learning'] = Quiz.objects.filter(visible_on_home=True, learning_purpose=True)
        return context


class Error404View(TemplateView):
    template_name = 'wsite/404.html'

