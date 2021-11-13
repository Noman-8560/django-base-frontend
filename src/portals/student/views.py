from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)

from src.application.models import (
    Article, Subject, Profile, Quiz, Question, QuestionStatement, QuestionChoice, QuestionImage, QuestionAudio,
    QuizQuestion, ChoiceVisibility, ImageVisibility, StatementVisibility, AudioVisibility, Screen, Team, QuizCompleted,
    Attempt, LearningResourceResult,
)

student_decorators = [login_required]

"""  VIEWS ======================================================================== """


class DashboardView(View):

    def get(self, request):
        allow = False

        # ALL_QUIZES
        all_quizes = Quiz.objects.filter(learning_purpose=False).order_by('-start_time')
        my_teams = Team.objects.filter(participants__in=[request.user.id])
        my_quizes = Quiz.objects.filter(id__in=my_teams.values_list('quiz', flat=True))

        # AVAILABLE_QUIZES
        available_quizes = Quiz.objects.filter(
            end_time__gte=timezone.now(),
            learning_purpose=False,
            start_time__lte=timezone.now()) \
            .order_by('-start_time')

        completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id, quiz__end_time__lt=timezone.now())

        # QUIZ ENROLLED
        enrolled_quizes = Quiz.objects \
            .filter(end_time__gt=timezone.now(), learning_purpose=False, id__in=my_quizes.values_list('id', flat=True)) \
            .exclude(id__in=completed_by_me.values_list('quiz', flat=True)).order_by('-start_time')

        # QUIZ SUBMITTED
        completed = Quiz.objects.filter(pk__in=completed_by_me.values_list('quiz', flat=True), learning_purpose=False)
        context = {
            'allow': allow,
            'quizes_all': all_quizes,  # QUIZ=> REQUIRED(current, upcoming)
            'quizes_available': available_quizes,  # QUIZ=> REQUIRED(upcoming, not_enrolled)
            'quizes_enrolled': enrolled_quizes,
            # QUIZ=> REQUIRED(upcoming, not_attempted)[CHECK_MODEL = QuizCompleted]
            'quizes_completed': completed_by_me  # QUIZ=> REQUIRED(Attempted)
        }

        if request.GET.get('quiz'):
            try:
                allow = True
                quiz = Quiz.objects.get(pk=int(request.GET.get('quiz')))

                questions = quiz.questions.all()
                user = User.objects.get(username=request.user.username)
                user_attempts = Attempt.objects.filter(user=user, quiz=quiz)
                teams = []

                # USER_REQUIREMENTS
                user_total_correct = []
                user_total_incorrect = []
                user_time_spent = []
                user_total_pass = []

                # OVER_ALL_REQUIREMENTS
                correct_attempts_all = []
                incorrect_attempts_all = []

                average_correct_attempts_all = []
                average_incorrect_attempts_all = []
                pass_attempts_all = []
                average_pass_attempts_all = []

                time_max = []
                time_min = []
                time_avg = []
                my_team_time = []

                for question in questions:
                    pass_attempts_all.append(1)
                    average_pass_attempts_all.append(1)
                    _attempts = Attempt.objects.filter(question=question).values('team').distinct()
                    _s_attempts = _attempts.filter(successful=True)
                    _u_attempts = _attempts.filter(successful=False)
                    temp_denominator = _s_attempts.count() + _u_attempts.count()

                    # GET TIMES -------------------------------------------------------------------------------------
                    _all_time_sum = 0
                    _max_time = 0
                    _min_time = 1000
                    count = 0
                    for v in _attempts.values('start_time', 'end_time', 'team', 'question'):
                        current = (v['end_time'] - v['start_time']).total_seconds()
                        if current < _max_time:
                            _max_time = _max_time
                        else:
                            _max_time = current

                        if current < _min_time:
                            _min_time = current
                        else:
                            _min_time = _min_time
                        count += 1

                        _all_time_sum += int(current)

                    time_max.append(int(_max_time))
                    time_min.append(int(_min_time))
                    time_avg.append(_all_time_sum / count)

                    my_team_attempts = Attempt.objects.filter(question=question, user=user)
                    if my_team_attempts.exists():
                        for a in my_team_attempts:
                            my_team_time.append(int((a.end_time - a.start_time).total_seconds()))
                    else:
                        my_team_time.append(0)
                    # -----------------------------------------------------------------------------------------------

                    # CORRECT ALL and IN_CORRECT ALL ----------------------------------------------------------------
                    correct_attempts_all.append(_s_attempts.count())
                    incorrect_attempts_all.append(_u_attempts.count())
                    # -----------------------------------------------------------------------------------------------

                    # AVG CORRECT ALL and AVG IN_CORRECT ALL --------------------------------------------------------
                    average_correct_attempts_all.append(
                        _s_attempts.count() / temp_denominator if temp_denominator > 0 else 0)
                    average_incorrect_attempts_all.append(
                        _u_attempts.count() / temp_denominator if temp_denominator > 0 else 0)
                    # -----------------------------------------------------------------------------------------------

                for attempt in user_attempts:
                    if attempt.successful:
                        user_total_correct.append(1)
                        user_total_incorrect.append(0)
                    else:
                        user_total_correct.append(0)
                        user_total_incorrect.append(1)

                    user_time_spent.append((attempt.end_time - attempt.start_time).total_seconds())
                    user_total_pass.append(0)

                context = {
                    'allow': allow,
                    'questions': [question.pk for question in questions],

                    'user_total_correct': user_total_correct,
                    'user_total_incorrect': user_total_incorrect,
                    'user_time_spent': user_time_spent,
                    'user_total_pass': user_total_pass,

                    'correct_attempts_all': correct_attempts_all,
                    'incorrect_attempts_all': incorrect_attempts_all,
                    'pass_attempts_all': pass_attempts_all,

                    'time_max': time_max,
                    'time_min': time_min,
                    'time_avg': time_avg,
                    'my_team_time': my_team_time,

                    'average_correct_attempts_all': average_correct_attempts_all,
                    'average_incorrect_attempts_all': average_incorrect_attempts_all,
                    'average_pass_attempts_all': average_pass_attempts_all,

                    'quizes_all': all_quizes,  # QUIZ=> REQUIRED(current, upcoming)
                    'quizes_available': available_quizes,  # QUIZ=> REQUIRED(upcoming, not_enrolled)
                    'quizes_enrolled': enrolled_quizes,
                    # QUIZ=> REQUIRED(upcoming, not_attempted) [CHECK_MODEL = QuizCompleted]
                    'quizes_completed': completed_by_me  # QUIZ=> REQUIRED(Attempted)
                }
            except Quiz.DoesNotExist:
                allow = False
                messages.error(request, 'Requested quiz does not exists.')

        return render(request=request, template_name='student/dashboard.html', context=context)


class QuizListView(View):

    def get(self, request):
        # ALL_QUIZES
        all_quizes = Quiz.objects.filter(learning_purpose=False).order_by('-start_time')
        my_teams = Team.objects.filter(participants__in=[request.user.id])
        my_quizes = Quiz.objects.filter(id__in=my_teams.values_list('quiz', flat=True))

        # AVAILABLE_QUIZES
        available_quizes = Quiz.objects.filter(end_time__gte=timezone.now(), learning_purpose=False).exclude(
            id__in=my_quizes.values_list('id', flat=True)).order_by('-start_time')

        completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id, passed=F('total'))

        # QUIZ ENROLLED
        enrolled_quizes = Quiz.objects \
            .filter(end_time__gt=timezone.now(), learning_purpose=False, id__in=my_quizes.values_list('id', flat=True)) \
            .exclude(id__in=completed_by_me.values_list('quiz', flat=True)).order_by('-start_time')

        # QUIZ SUBMITTED
        completed = Quiz.objects.filter(pk__in=completed_by_me.values_list('quiz', flat=True), learning_purpose=False)

        context = {
            'quizes_all': all_quizes,  # QUIZ=> REQUIRED(current, upcoming)
            'quizes_available': available_quizes,  # QUIZ=> REQUIRED(upcoming, not_enrolled)
            'quizes_enrolled': enrolled_quizes,  # QUIZ=> REQUIRED(upcoming, not_attempted)[CHECK_MODEL = QuizCompleted]
            'quizes_completed': completed_by_me  # QUIZ=> REQUIRED(Attempted)
        }
        return render(request=request, template_name='student/quiz_list.html', context=context)


class TeamListView(View):

    def get(self, request):
        completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id)
        completed = Quiz.objects.filter(pk__in=completed_by_me.values_list('quiz', flat=True))

        teams = Team.objects.filter(participants__username=request.user.username)

        expired_teams = teams.filter(quiz__end_time__lt=timezone.now())
        available_teams = teams.filter(quiz__end_time__gt=timezone.now()).exclude(quiz__in=completed)

        context = {
            'teams': teams.order_by('-created_at'),
            'ex_teams': expired_teams.order_by('-created_at'),
            'av_teams': available_teams.order_by('-created_at'),
        }
        return render(request=request, template_name='application/teams.html', context=context)


class LearningResourceListView(View):

    def get(self, request):
        # ALL_QUIZES
        all_quizes = Quiz.objects.filter(learning_purpose=True).order_by('-start_time')

        # AVAILABLE_QUIZES
        available_quizes = Quiz.objects.filter(
            end_time__gte=timezone.now(),
            learning_purpose=True).order_by('-start_time')

        completed_by_me = LearningResourceResult.objects.filter(user__id=request.user.id).order_by('-created')

        context = {
            'all_quizes': all_quizes,
            'available_quizes': available_quizes,
            'completed_quizes': completed_by_me,
        }
        return render(request=request, template_name='student/learning_resource_list.html', context=context)


"""  ARTICLES --------------------------------------------------------------------- """

"""  SUBJECTS --------------------------------------------------------------------- """

""" QUESTION ---------------------------------------------------------------------- """

""" C-API ========================================================================= """

""" CHANGE ======================================================================== """
