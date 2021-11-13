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
    Attempt, LearningResourceResult, LearningResourceAttempts,
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


"""  LEARNING RESOURCE --------------------------------------------------------------------- """


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


class LearningResourceLiveView(View):

    def get(self, request, quiz_id):
        user_quiz = None
        allowed_to_start = False
        time_status = None
        question_ids = []

        """ QUIZ and TEAM is required here """
        try:
            user_quiz = Quiz.objects.get(pk=quiz_id)

            # if len(QuizCompleted.objects.filter(user=request.user, quiz=user_quiz)) > 0:
            # messages.success(request=request, message="Dear User you have already attempted this quiz, if you attempt it again your previous record will be updated")

        except Quiz.DoesNotExist:
            messages.error(request=request, message="Requested Quiz doesn't exists")
            return redirect('application:quizes', permanent=True)

        if not user_quiz.questions.all():
            messages.error(request=request,
                           message="Quiz is incomplete no questions are associated with this quiz - please consult admin")
            return redirect('application:quizes', permanent=True)

        if user_quiz.start_time <= timezone.now() < user_quiz.end_time:
            allowed_to_start = True
            time_status = 'present'

            questions = user_quiz.questions.all()
            for question in questions:
                question_ids.append(question.pk)

        else:
            if user_quiz.start_time > timezone.now():
                time_status = 'future'
            elif timezone.now() > user_quiz.end_time:
                time_status = 'past'

        context = {
            'time_status': time_status,
            'allowed_to_start': allowed_to_start,
            'quiz_start_date': user_quiz.start_time,
            'quiz_end_date': user_quiz.end_time,
            'question_ids': question_ids,
            'quiz_id': user_quiz.pk,
        }

        return render(request=request, template_name='application/learning_quiz.html', context=context)


class LearningResourceResultView(View):

    def get(self, request, quiz_id):
        quiz = None
        result = None

        try:
            quiz = Quiz.objects.get(pk=quiz_id)
            result = LearningResourceResult.objects.get(user=request.user, quiz=quiz)
        except LearningResourceResult.DoesNotExist:
            pass
        except Quiz.DoesNotExist:
            pass

        attempts = LearningResourceAttempts.objects.filter(user=request.user, quiz=quiz)

        context = {
            'quiz': quiz,
            'result': result,
            'attempts': attempts
        }
        return render(request=request, template_name='application/learning_quiz_result.html', context=context)


"""  SUBJECTS --------------------------------------------------------------------- """

""" QUESTION ---------------------------------------------------------------------- """

""" C-API ========================================================================= """


class LearningResourceLiveQuestionSubmitJSON(View):
    def get(self, request):
        success = False
        message = None
        end = False

        """ CHECK API CALL """
        if request.method == 'POST':

            quiz = Quiz.objects.get(pk=request.POST['quiz_id'])

            question = Question.objects.get(pk=request.POST['question_id'])
            choice_id = request.POST['choice_id']

            """ CHECK CORRECT OR NOT """
            correct = QuestionChoice.objects.get(pk=choice_id).is_correct

            """------------------------------------------------------------"""
            """                     SAVING DATA                            """
            """------------------------------------------------------------"""

            learn_previous = LearningResourceResult.objects.filter(user=request.user, quiz=quiz)
            if len(learn_previous) == 0:
                LearningResourceAttempts(
                    question=question,
                    user=request.user,
                    quiz=quiz,
                    start_time=request.POST['start_time'],
                    end_time=request.POST['end_time'],
                    successful=correct
                ).save()
            else:
                x = LearningResourceAttempts.objects.filter(question=question, user=request.user, quiz=quiz)[0]
                x.start_time = request.POST['start_time']
                x.end_time = request.POST['end_time']
                x.successful = correct
                x.save()

            if request.POST['end'] == 'True':
                yy = LearningResourceAttempts.objects.filter(user=request.user, quiz=quiz)

                if len(learn_previous) == 0:
                    LearningResourceResult(
                        user=request.user,
                        quiz=quiz,
                        total=yy.count(),
                        obtained=yy.filter(successful=True).count()
                    ).save()
                else:
                    y = LearningResourceResult.objects.filter(user=request.user, quiz=quiz)[0]
                    y.total = yy.count()
                    y.obtained = yy.filter(successful=True).count()
                    y.attempts = y.attempts + 1
                    y.save()

            success = True
            message = f"Question {request.POST['question_id']} marked successfully"

            response = {
                'success': success,
                'message': message,
                'end': request.POST['end'],
                'path': request.get_full_path()
            }

            return JsonResponse(data=response, safe=False)


class LearningResourceLiveQuestionAccessJSON(View):

    def get(self, request, quiz_id, question_id):
        total = 0
        attempts = 0
        remains = 0

        statements = []
        images = []
        audios = []
        choices_keys = []
        choices_values = []

        if request.method == 'GET':

            ''' __FETCHING BASE DATA__'''
            quiz = Quiz.objects.get(pk=quiz_id)

            '''__QUESTION LOGIC WILL BE HERE__'''
            question = quiz.questions.get(pk=question_id)

            '''__FETCHING SUBMISSION AND CHOICES CONTROL__'''

            ''' __FETCHING IMAGES AUDIOS CHOICES AND STATEMENTS__'''
            [statements.append(x.statement) for x in question.questionstatement_set.all()]
            [images.append(y.image.url) if y.url is None else images.append(y.url) for y in
             question.questionimage_set.all()]
            [audios.append(z.audio) if z.url is None else audios.append(z.url) for z in
             question.questionaudio_set.all()]
            [choices_keys.append(c['pk']) for c in question.questionchoice_set.all().values('pk')]
            [choices_values.append(c['text']) for c in question.questionchoice_set.all().values('text')]

            total = quiz.questions.count()
            attempts = LearningResourceAttempts.objects.filter(user=request.user, quiz=quiz).count()
            remains = total - attempts

            ''' __GENERATING RESPONSES__'''
            response = {
                'question': question.pk,
                'choices_keys': choices_keys,
                'choices_values': choices_values,
                'statements': statements,
                'images': images,
                'audios': audios,

                'total': total,
                'attempts': attempts,
                'remains': remains,
            }
            return JsonResponse(data=response, safe=False)
        else:
            return JsonResponse(data=None, safe=False)


""" CHANGE ======================================================================== """
