from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)
from src.application.models import (
    Article, Subject,
)


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

