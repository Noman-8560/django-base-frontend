from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)

from src.application.forms import ProfileSchoolForm
from src.application.models import (
    Article, Subject, Profile, Quiz,
)
from src.portals.admins.forms import ProfileBasicForm, ProfileParentForm, ProfileImageForm, ProfileOtherForm, QuizForm

"""  INIT ------------------------------------------------------------------------- """


class DashboardView(TemplateView):
    template_name = 'admins/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


"""  ARTICLES --------------------------------------------------------------------- """


class ArticleListView(ListView):
    models = Article
    queryset = Article.objects.all()
    template_name = 'admins/article_list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(ArticleListView, self).dispatch(*args, **kwargs)


class ArticleDetailView(DetailView):
    models = Article
    queryset = Article.objects.all()
    template_name = 'admins/article_detail.html'


class ArticleCreateView(CreateView):
    models = Article
    queryset = Article.objects.all()
    fields = '__all__'
    template_name = 'admins/article_create_form.html'
    success_url = reverse_lazy('admin-portal:article')


class ArticleUpdateView(UpdateView):
    models = Article
    queryset = Article.objects.all()
    fields = '__all__'
    template_name = 'admins/article_create_form.html'
    success_url = reverse_lazy('admin-portal:article')


class ArticleDeleteView(DeleteView):
    models = Article
    queryset = Article.objects.all()
    template_name = 'admins/article_delete.html'
    success_url = reverse_lazy('admin-portal:article')


"""  SUBJECTS --------------------------------------------------------------------- """


class SubjectListView(ListView):
    models = Subject
    queryset = Subject.objects.all()
    template_name = 'admins/subject_list.html'


class SubjectDetailView(DetailView):
    models = Subject
    queryset = Subject.objects.all()
    template_name = 'admins/subject_detail.html'


class SubjectCreateView(CreateView):
    models = Subject
    queryset = Subject.objects.all()
    fields = '__all__'
    template_name = 'admins/subject_create_form.html'
    success_url = reverse_lazy('admin-portal:subject')


class SubjectUpdateView(UpdateView):
    models = Subject
    queryset = Subject.objects.all()
    fields = '__all__'
    template_name = 'admins/subject_create_form.html'
    success_url = reverse_lazy('admin-portal:subject')


class SubjectDeleteView(DeleteView):
    models = Subject
    queryset = Subject.objects.all()
    template_name = 'admins/subject_delete.html'
    success_url = reverse_lazy('admin-portal:subject')


""" USER """


class QuizListView(ListView):
    models = Quiz
    queryset = Quiz.objects.all()
    template_name = 'admins/quiz_list.html'


class QuizCreateView(CreateView):
    models = Quiz
    queryset = Quiz.objects.all()
    fields = '__all__'
    template_name = 'admins/quiz_create_form.html'
    success_url = reverse_lazy('admin-portal:quiz')


class QuizUpdateView(UpdateView):
    models = Quiz
    queryset = Quiz.objects.all()
    fields = '__all__'
    template_name = 'admins/quiz_update_form.html'
    success_url = reverse_lazy('admin-portal:quiz')


class QuizDeleteView(DeleteView):
    models = Quiz
    queryset = Quiz.objects.all()
    template_name = 'admins/quiz_delete.html'
    success_url = reverse_lazy('admin-portal:quiz')

