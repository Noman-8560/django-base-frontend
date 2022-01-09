from django.core.paginator import Paginator
from django.views.generic import TemplateView, ListView

from src.application.models import Quiz
from src.portals.admins.filters import QuizFilter


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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(QuizListView, self).get_context_data(**kwargs)
        quiz_filter = QuizFilter(self.request.GET, self.get_queryset())
        context['quiz_filter_form'] = quiz_filter.form

        paginator = Paginator(quiz_filter.qs, 12)
        page_number = self.request.GET.get('page')
        quiz_page_object = paginator.get_page(page_number)

        context['quiz_list'] = quiz_page_object
        return context


class LearningListView(ListView):
    template_name = 'wsite/learning_list.html'

    def get_queryset(self):
        return Quiz.objects.filter(learning_purpose=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(LearningListView, self).get_context_data(**kwargs)
        quiz_filter = QuizFilter(self.request.GET, self.get_queryset())
        context['quiz_filter_form'] = quiz_filter.form

        paginator = Paginator(quiz_filter.qs, 12)
        page_number = self.request.GET.get('page')
        quiz_page_object = paginator.get_page(page_number)

        context['quiz_list'] = quiz_page_object
        return context


class PrivacyPolicyView(TemplateView):
    template_name = 'wsite/policy.html'


class TermsAndConditionsView(TemplateView):
    template_name = 'wsite/terms.html'


class ContactView(TemplateView):
    template_name = 'wsite/contact.html'


class Error404View(TemplateView):
    template_name = 'wsite/404.html'
