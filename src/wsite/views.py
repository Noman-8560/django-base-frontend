from django.views.generic import TemplateView, ListView

from src.application.models import Quiz


class HomeView(TemplateView):
    template_name = 'wsite/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['quizzes'] = Quiz.objects.filter(visible_on_home=True, learning_purpose=False)
        context['learning'] = Quiz.objects.filter(visible_on_home=True, learning_purpose=True)
        return context


class QuizListView(ListView):
    template_name = 'wsite/quiz_list.html'

    def get_queryset(self):
        return Quiz.objects.filter(learning_purpose=False)


class LearningListView(ListView):
    template_name = 'wsite/learning_list.html'

    def get_queryset(self):
        return Quiz.objects.filter(learning_purpose=True)


class Error404View(TemplateView):
    template_name = 'wsite/404.html'

