from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    ListView, UpdateView, DeleteView, CreateView, DetailView
)

from src.application.forms import QuestionImageForm
from src.application.models import (
    Quiz, QuizQuestion, Question, ChoiceVisibility, StatementVisibility, ImageVisibility,
    AudioVisibility,
    Subject, QuestionStatement, QuestionChoice, QuestionAudio, QuestionImage)
from src.portals.admins.dll import QuestionDS
from src.portals.admins.forms import QuizQuestionForm, QuestionAudioForm


""" QUIZ """
@method_decorator(login_required, name='dispatch')
class QuizListView(ListView):
    models = Quiz
    queryset = Quiz.objects.all()
    template_name = 'moderator/quiz_list.html'

    def get_queryset(self):
        return Quiz.objects.all()


@method_decorator(login_required, name='dispatch')
class QuizCreateView(CreateView):
    models = Quiz
    queryset = Quiz.objects.all()
    fields = '__all__'
    template_name = 'moderator/quiz_create_form.html'
    success_url = reverse_lazy('admin-portal:quiz')


@method_decorator(login_required, name='dispatch')
class QuizUpdateView(UpdateView):
    models = Quiz
    queryset = Quiz.objects.all()
    fields = '__all__'
    template_name = 'moderator/quiz_update_form.html'
    success_url = reverse_lazy('admin-portal:quiz')


@method_decorator(login_required, name='dispatch')
class QuizDeleteView(DeleteView):
    models = Quiz
    queryset = Quiz.objects.all()
    template_name = 'moderator/quiz_delete.html'
    success_url = reverse_lazy('admin-portal:quiz')


@method_decorator(login_required, name='dispatch')
class QuizDetailView(DetailView):
    template_name = 'admins/quiz_detail.html'
    model = Quiz

    def get_context_data(self, **kwargs):
        context = super(QuizDetailView, self).get_context_data(**kwargs)
        quiz = self.object

        quiz_questions = QuizQuestion.objects.filter(quiz=quiz)
        questions = Question.objects.filter(subject__in=quiz.subjects.all(), age_limit__lte=quiz.age_limit)
        total = questions.count()
        questions = questions.exclude(id__in=quiz_questions.values_list('question__id', flat=True))

        questionsDS = []
        for quiz_question in quiz_questions:

            question_exists = False
            if quiz_question.question in quiz.questions.all():
                question_exists = True

            questionDS = QuestionDS(
                id=quiz_question.pk, question_id=quiz_question.question.pk, question_exists=question_exists,
                level=quiz_question.question.level, subject=quiz_question.question.subject,
                question_type=quiz_question.question.question_type, age_limit=quiz_question.question.age_limit,
                submission_control=quiz_question.submission_control
            )

            for choice_v in ChoiceVisibility.objects.filter(
                    quiz_question=quiz_question, quiz_question__quiz=quiz):
                questionDS.add_choice(
                    id=choice_v.id, description=choice_v.choice.text, is_correct=choice_v.choice.is_correct,
                    screen1=choice_v.screen_1, screen2=choice_v.screen_2, screen3=choice_v.screen_3
                )

            for statement_v in StatementVisibility.objects.filter(
                    quiz_question=quiz_question, quiz_question__quiz=quiz):
                questionDS.add_statment(
                    id=statement_v.id, description=statement_v.statement.statement,
                    screen1=statement_v.screen_1, screen2=statement_v.screen_2, screen3=statement_v.screen_3
                )

            for image_v in ImageVisibility.objects.filter(
                    quiz_question=quiz_question, quiz_question__quiz=quiz):
                if image_v.image.image:
                    questionDS.add_image(
                        id=image_v.id, url=image_v.image.url, image=image_v.image.image.url,
                        screen1=image_v.screen_1, screen2=image_v.screen_2, screen3=image_v.screen_3
                    )
                else:
                    questionDS.add_image(
                        id=image_v.id, url=image_v.image.url, image=None,
                        screen1=image_v.screen_1, screen2=image_v.screen_2, screen3=image_v.screen_3
                    )

            for audio_v in AudioVisibility.objects.filter(
                    quiz_question=quiz_question, quiz_question__quiz=quiz):
                if audio_v.audio.audio:
                    questionDS.add_audio(
                        id=audio_v.id, url=audio_v.audio.url, audio=audio_v.audio.audio.url,
                        screen1=audio_v.screen_1, screen2=audio_v.screen_2, screen3=audio_v.screen_3
                    )
                else:
                    questionDS.add_audio(
                        id=audio_v.id, url=audio_v.audio.url, audio=None,
                        screen1=audio_v.screen_1, screen2=audio_v.screen_2, screen3=audio_v.screen_3
                    )

            questionsDS.append(questionDS)

        context = {
            'questionDS': questionsDS,
            'questions': questions,
            'subjects': quiz.subjects.all(),
            'form': QuizQuestionForm(instance=QuizQuestion.objects.first()),
            'quiz_id': quiz.pk,
            'quiz_title': quiz.title,
            'total': total,
            'selected': quiz.questions.count(),
            'remaining': questions.count(),
            'players': quiz.players,
        }

        return context


""" QUESTION """


@method_decorator(login_required, name='dispatch')
class QuestionListView(ListView):
    models = Question
    queryset = Question.objects.all()
    template_name = 'admins/question_list.html'


@method_decorator(login_required, name='dispatch')
class QuestionDeleteView(DeleteView):
    models = Question
    queryset = Question.objects.all()
    template_name = 'admins/question_delete.html'
    success_url = reverse_lazy('admin-portal:question')


@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
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