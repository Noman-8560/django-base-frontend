from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)

from src.application.forms import ProfileSchoolForm
from src.application.models import (
    Article, Subject, Profile, Quiz, Question, QuestionStatement, QuestionChoice, QuestionImage, QuestionAudio,
)
from src.portals.admins.forms import ProfileBasicForm, ProfileParentForm, ProfileImageForm, ProfileOtherForm, QuizForm, \
    QuestionImageForm, QuestionAudioForm


# decorators = [never_cache, login_required]
# @method_decorator(decorators, name='dispatch')

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


""" QUIZ -------------------------------------------------------------------------- """


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


""" QUESTION ---------------------------------------------------------------------- """


class QuestionListView(ListView):
    models = Question
    queryset = Question.objects.all()
    template_name = 'admins/question_list.html'


class QuestionDeleteView(DeleteView):
    models = Question
    queryset = Question.objects.all()
    template_name = 'admins/question_delete.html'
    success_url = reverse_lazy('admin-portal:question')


class QuestionCreateView(View):

    def get(self, request):
        question_subjects = Subject.objects.all()
        context = {'subjects': question_subjects}
        return render(request=request, template_name='admins/question_add_form.html', context=context)

    def post(self, request):
        question = Question.objects.create(
            age_limit=request.POST['age'],
            subject=Subject.objects.get(pk=request.POST['subject_id']),
        )

        for statement in request.POST.getlist('statements[]'):
            QuestionStatement.objects.create(
                statement=statement,
                question=question
            )

        corrects = request.POST.getlist('corrects[]')
        options = request.POST.getlist('options[]')

        for index, value in enumerate(options):

            choice = False
            if corrects[index] == '1':
                choice = True

            QuestionChoice.objects.create(
                text=options[index],
                is_correct=choice,
                question=question
            )

        return JsonResponse(data={'message': 'success', 'question': question.pk}, safe=False)


class QuestionUpdateView(View):

    def get(self, request, pk):
        question = get_object_or_404(Question, pk=pk)
        context = {
            'statements': QuestionStatement.objects.filter(question=question),
            'choices': QuestionChoice.objects.filter(question=question),
            'images': QuestionImage.objects.filter(question=question),
            'audios': QuestionAudio.objects.filter(question=question),
            'question_id': question.pk,
            'question': question,
            'subjects': Subject.objects.all(),
            'image_form': QuestionImageForm(),
            'audio_form': QuestionAudioForm(),
        }
        return render(request=request, template_name='admins/question_update_form.html', context=context)


""" C-API ------------------------------------------------------------------------- """
""" QUESTION RELATED ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ """


class QuestionStatementAddJSON(View):

    def post(self, request):
        text = request.POST['text']
        # screen = request.POST['screen']
        question_id = request.POST['pk']
        statement = QuestionStatement()
        statement.statement = text
        # statement.screen = Screen.objects.get(no=screen)
        statement.question = Question.objects.get(pk=question_id)
        statement.save()
        response = {
            'statement': text
        }
        return JsonResponse(data=response, safe=False)


class QuestionStatementDeleteJSON(View):

    def get(self, request, pk):
        QuestionStatement.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)


class QuestionChoiceAddJSON(View):

    def post(self, request):
        is_correct = str(request.POST['is_correct']) == 'true'
        question_id = request.POST['pk']
        text = request.POST['text']
        choice = QuestionChoice()
        choice.text = text
        choice.question = Question.objects.get(pk=question_id)
        choice.is_correct = is_correct
        choice.save()
        response = {'choice': text}
        return JsonResponse(data=response, safe=False)


class QuestionChoiceDeleteJSON(View):

    def get(self, request, pk):
        QuestionChoice.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)


""" CHNAGE """