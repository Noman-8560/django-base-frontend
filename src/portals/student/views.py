import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView
from notifications.signals import notify

from cocognite import settings
from src.application.models import (
    Quiz, Question, QuestionChoice,
    QuizQuestion, Screen, Team, QuizCompleted,
    Attempt, LearningResourceResult, LearningResourceAttempts,
    Relation)
from src.portals.student.dll import identify_user_in_team
from src.portals.student.forms import TeamForm
from src.portals.student.helpers import generate_signature
from src.zoom_api.views import zoom_create_meeting, zoom_delete_meeting
User = get_user_model()

student_decorators = [login_required]

"""  VIEWS ================================================================================= """


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


class TeamDetailView(View):

    def get(self, request, pk):
        team = None
        try:
            team = Team.objects.get(pk=pk)

        except Team.DoesNotExist:
            messages.error(request=request, message=f'Requested Team with [ ID:{pk} ] does not exists.')
            return HttpResponseRedirect(reverse('student-portal:team'))

        context = {
            'team': team,
            'players': team.participants.all()
        }
        return render(request=request, template_name='student/team.html', context=context)


class TeamDeleteView(View):

    def get(self, request, pk):
        team = None

        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            messages.error(request=request, message="Requested Team Does not exists")
            return redirect('student-portal:team', permanent=True)

        if len(Team.objects.filter(participants__username=request.user.username, pk=pk)) == 0:
            messages.error(request=request, message="You are not allowed to delete this team")
            return redirect('student-portal:team', permanent=True)

        completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id)
        completed = Quiz.objects.filter(pk__in=completed_by_me.values_list('quiz', flat=True))

        if Team.objects.filter(quiz__in=completed):
            messages.error(request=request,
                           message="you have attempted quiz with this team, you are not allowed to delete this team now")
            return redirect('student-portal:team', permanent=True)
        else:
            zoom_delete_meeting(team.zoom_meeting_id)
            team.delete()
            messages.success(request=request,
                             message="Team Destroyed completely")
        return redirect('student-portal:team', permanent=True)


class QuizEnrollView(View):

    def get(self, request, pk):
        # CHECK_QUIZ_EXISTS

        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            messages.error(request=request, message=f'Requested Quiz with [ ID:{pk} ]does not exists.')
            return HttpResponseRedirect(reverse('student-portal:quiz'))

        # ALREADY_ALLOCATED
        if Team.objects.filter(participants__username=request.user.username, quiz=quiz).count() != 0:
            messages.warning(request=request, message=f'You are already enrolled to this quiz')
            return HttpResponseRedirect(reverse('student-portal:quiz'))

        context = {
            'quiz': quiz,
            'form': TeamForm()
        }
        return render(request=request, template_name='student/team_create_form.html', context=context)

    def post(self, request, pk):
        # CHECK_QUIZ_EXISTS
        quiz = None
        try:
            quiz = Quiz.objects.get(pk=pk)
        except Quiz.DoesNotExist:
            messages.error(request=request, message=f'Requested Quiz with [ ID:{pk} ]does not exists.')
            return HttpResponseRedirect(reverse('student-portal:quiz'))

        # ALREADY_ALLOCATED
        if Team.objects.filter(participants__username=request.user.username, quiz=quiz).count() != 0:
            messages.warning(request=request, message=f'You are already enrolled to this quiz')
            return HttpResponseRedirect(reverse('student-portal:quiz'))

        # POST_METHOD
        if request.method == 'POST':
            team_name = request.POST['team_name']
            player_1 = request.user
            player_2 = None
            player_3 = None

            # 2 player quiz ---------------------------------------------
            if quiz.players == '2':
                user2 = User.objects.filter(username=request.POST['player_2'])

                if not user2:
                    pass

                player_2 = user2[0]

            # 3 player quiz ---------------------------------------------
            if quiz.players == '3':
                pass

            # USER_EXISTS_OR_NOT
            try:

                if quiz.players == '2':

                    player_2 = User.objects.get(username=request.POST['player_2'])
                    if quiz.players == '3':
                        player_3 = User.objects.get(username=request.POST['player_3'])

                        # PLAYER_3_ASSIGNED_OR_NOT
                        if Team.objects.filter(participants__username=player_3.username, quiz=quiz).count() != 0:
                            messages.warning(
                                request=request, message=f'Requested participant or participants '
                                                         f'already enrolled choose different partners.'
                            )
                            return HttpResponseRedirect(reverse('application:enroll_quiz', args=(quiz.pk,)))

                    # PLAYER_3_ASSIGNED_OR_NOT
                    if Team.objects.filter(participants__username=player_2.username, quiz=quiz).count() != 0:
                        messages.warning(request=request,
                                         message=f'Requested participant or participants '
                                                 f'already enrolled choose different partners.'
                                         )
                        return HttpResponseRedirect(reverse('application:enroll_quiz', args=(quiz.pk,)))

            except User.DoesNotExist:
                messages.error(request=request, message=f'Requested participant or participants does not exists.')
                return HttpResponseRedirect(reverse('application:enroll_quiz', args=(quiz.pk,)))

            #  --------- MEETING --------- #

            meeting_id = None
            start_url = None
            join_url = None

            if int(quiz.players) > 1:
                """response = zoom_create_meeting(name=f"QUIZ {quiz.title} - TEAM {team_name}",
                                               start_time=quiz.start_time.timestamp(),
                                               end_time=quiz.end_time.timestamp(), host=request.user.email)
                if response.status_code != 201:
                    messages.error(request=request,
                                   message=f'Failed To create zoom meeting please consult administration')
                    return HttpResponseRedirect(reverse('application:enroll_quiz', args=(quiz.pk,)))

                meeting = json.loads(response.text)
                meeting_id = meeting['id']
                start_url = meeting['start_url']
                join_url = meeting['join_url']"""

            # --------- SAVE --------- #

            team = Team(
                name=team_name,
                quiz=quiz,
                created_by=request.user,
                zoom_meeting_id=meeting_id,
                zoom_start_url=start_url,
                zoom_join_url=join_url,
            )

            team.save()
            team.participants.add(player_1, player_2, player_3)
            messages.success(request=request, message=f'You have successfully enrolled to quiz={quiz.title} '
                                                      f'with team={team_name} as a caption of team.')

            # ---------> NOTIFY
            ps = [request.user.username]
            if player_2 is not None:
                ps.append(player_2.username)
            if player_3 is not None:
                ps.append(player_3.username)

            for user in ps:
                desc = f"<b>Hi {user}!</b> you have registered to take part in <b>{quiz.title}</b>, " \
                       f"scheduled on <b>{quiz.start_time.ctime()}</b>" \
                       f" your team is <b>{team.name}</b> and members are {', '.join([str(elem) for elem in ps])}."

                notify.send(
                    request.user,
                    recipient=User.objects.get(pk=user.pk),
                    verb=f'Enrolled to {quiz.title}',
                    level='success',
                    description=desc
                )
            # -----------------------------------------------------------------------------------------------------------
            return HttpResponseRedirect(reverse('student-portal:quiz'))

        # GET_METHOD
        context = {
            'quiz': quiz,
            'form': TeamForm()
        }
        return render(request=request, template_name='student/team_create_form.html', context=context)


class QuizLiveView(View):

    def get(self, request, pk):
        user_team = None
        user_quiz = None
        allowed_to_start = False
        time_status = None
        question_ids = []
        user_no = None
        submission = None
        new = False

        ''' QUIZ and TEAM is required here'''

        try:
            user_quiz = Quiz.objects.get(pk=pk)
            questions = user_quiz.questions.all()
            user_team = Team.objects.filter(quiz=pk, participants=request.user)[0]
            if not user_team:
                messages.error(request=request,
                               message="You are not registered to any team _ please register your team first")
                return redirect('student-portal:quiz', permanent=True)

            completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id, passed=F('total'))
            if completed_by_me:
                messages.error(request=request, message="Dear User you have already attempted this quiz")
                return redirect('student-portal:quiz', permanent=True)

        except Quiz.DoesNotExist:
            messages.error(request=request, message="Requested Quiz doesn't exists")
            return redirect('student-portal:quiz', permanent=True)

        if not user_quiz.questions.all():
            messages.error(request=request,
                           message="Quiz is incomplete no questions are associated with this quiz - please consult admin")
            return redirect('student-portal:quiz', permanent=True)

        if user_quiz.start_time <= timezone.now() < user_quiz.end_time:
            allowed_to_start = True
            time_status = 'present'

            attempts = Attempt.objects.filter(quiz=user_quiz, user=request.user)

            remaining = questions.exclude(id__in=attempts.values_list('question', flat=True))
            for re in remaining:
                question_ids.append(re.pk)
            user_no = identify_user_in_team(user_team, request, user_quiz)

            no_notify = False

            if not QuizCompleted.objects.filter(user=request.user, quiz=pk):
                for user in user_team.participants.all():
                    QuizCompleted(
                        user=user, quiz=user_quiz, remains=','.join(map(str, question_ids)),
                        total=user_quiz.questions.count()
                    ).save()
                    if user != request.user:
                        if user != request.user:
                            notify.send(
                                request.user,
                                recipient=user,
                                verb=f'Quiz {user_quiz.title} Started',
                                level='info',
                                description=f"<b>Hi {user.username}!</b> <b>{request.user}</b> "
                                            f"has started the quiz join your teammates ASAP"
                            )
                no_notify = True

            if not no_notify:
                for user in user_team.participants.all():
                    if user != request.user:
                        notify.send(
                            request.user,
                            recipient=user,
                            verb=f'Teammate joined {user_quiz.title}',
                            level='info',
                            description=f"<b>Hi {user.username}!</b> your teammate <b>{request.user}</b> "
                                        f"has joined the quiz"
                        )

            submission = '1'

        else:
            if user_quiz.start_time > timezone.now():
                time_status = 'future'
            elif timezone.now() > user_quiz.end_time:
                time_status = 'past'

        zoom_start_url = f"https://zoom.us/s/{user_team.zoom_meeting_id}"
        zoom_join_url = f"https://zoom.us/j/{user_team.zoom_meeting_id}"

        context = {
            'time_status': time_status,
            'allowed_to_start': allowed_to_start,
            'quiz_start_date': user_quiz.start_time,
            'quiz_end_date': user_quiz.end_time,
            'question_ids': question_ids,
            'team_id': user_team.pk,
            'zoom_join_url': zoom_start_url if user_team.created_by == request.user else zoom_join_url,
            'zoom_start_url': user_team.zoom_start_url,
            'quiz_id': user_quiz.pk,
            'user_no': user_no,
            'submission_control': submission,
            'quiz': Quiz.objects.get(pk=pk)
        }

        return render(request=request, template_name='student/quiz_live.html', context=context)


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
        return render(request=request, template_name='student/team_list.html', context=context)


"""  RELATION LIST --------------------------------------------------------------------- """


class RelationListView(ListView):
    model = Relation
    template_name = 'student/relation_list.html'

    def get_queryset(self):
        return Relation.objects.filter(child=self.request.user, is_verified_by_child=True)

    def get_context_data(self, **kwargs):
        context = super(RelationListView, self).get_context_data(**kwargs)
        context['relation_list_unverified'] = Relation.objects.filter(
            child=self.request.user, is_verified_by_child=False
        )
        return context


class RelationDetailView(View):

    def get(self, request, pk):
        relation = get_object_or_404(Relation.objects.filter(child=self.request.user), pk=pk)
        context = {'relation': relation}
        return render(request, 'student/relation_detail.html', context)

    def post(self, request, pk):
        relation_ = get_object_or_404(Relation.objects.filter(child=self.request.user), pk=pk)
        if relation_.is_verified_by_child:
            relation_.delete()
            messages.success(
                request, f"You have successfully verified {relation_.parent.username} "
                         f"as your {relation_.relation}"
            )
            return redirect('student-portal:relation')

        relation_.is_verified_by_child = True
        relation_.save()
        messages.success(
            request, f"You have successfully removed access from {relation_.parent.username} "
                     f"identified as your {relation_.relation}"
        )
        return redirect('student-portal:relation-detail', pk)


class RelationDeleteView(DeleteView):
    template_name = 'student/relation_delete.html'
    model = Relation
    success_url = reverse_lazy('student-portal:relation')

    def get_object(self, queryset=None):
        return get_object_or_404(Relation.objects.filter(child=self.request.user), pk=self.kwargs['pk'])


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
            return redirect('student-portal:quiz', permanent=True)

        if not user_quiz.questions.all():
            messages.error(request=request,
                           message="Quiz is incomplete no questions are associated with this quiz - please consult admin")
            return redirect('student-portal:quiz', permanent=True)

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

        return render(request=request, template_name='student/learning_resource_live.html', context=context)


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
        return render(request=request, template_name='student/learning_resource_result.html', context=context)


"""  EXTRA VIEWS ---------------------------------------------------------------------------- """


class ZoomMeetingView(View):

    def get(self, request, quiz_id):
        user_quiz = Quiz.objects.get(pk=quiz_id)
        user_team = Team.objects.filter(quiz=user_quiz, participants=request.user)[0]
        data = {
            'apiKey': "EBB0k1HnRN6hlD5dvrkAyw",
            'apiSecret': "1hnrKhnDfgbZDsg5WdLKxEIA9bZsPBm2BKOF",
            'meetingNumber': user_team.zoom_meeting_id,
            'role': 1
        }
        signature = generate_signature(data)

        context = {
            'meeting': user_team.zoom_meeting_id,
            'signature': signature,
            'user_name': request.user.username,
            'user_email': request.user.email,
            'api_key': settings.ZOOM_API_KEY_JWT,
        }

        return render(request=request, template_name='student/zoom_meeting.html', context=context)


""" C-API =================================================================================== """


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


class QuizLiveQuestionSubmitJSON(View):

    def post(self, request):
        success = False
        message = None
        end = False

        quiz = Quiz.objects.get(pk=request.POST['quiz_id'])
        question = Question.objects.get(pk=request.POST['question_id'])
        team = Team.objects.get(pk=request.POST['team_id'])
        choice = QuestionChoice.objects.get(pk=request.POST['choice_id'])

        users = team.participants.all()
        attempt = Attempt.objects.filter(user=request.user, question=question, quiz=quiz)

        for user in users:

            Attempt(
                quiz=quiz, user=user, question=question, team=team,
                start_time=request.POST['start_time'], end_time=request.POST['end_time'],
                successful=choice.is_correct
            ).save()

            quiz_complete = QuizCompleted.objects.filter(quiz=quiz, user=user)[0]
            quiz_complete.passed += 1
            u = quiz_complete.remains.split(',')
            u = [int(i) for i in u]
            u.pop(0)
            u = ','.join([str(elem) for elem in u])
            quiz_complete.remains = u

            if choice.is_correct:
                quiz_complete.obtained += 1

            quiz_complete.save()

            if int(request.POST['end']) == 1:
                meeting_id = team.zoom_meeting_id
                if meeting_id is not None or meeting_id == '':
                    zoom_delete_meeting(meeting_id)

                notify.send(
                    request.user,
                    recipient=user,
                    verb=f'Quiz {quiz.title} submitted',
                    level='info',
                    description=f'<b>Hi {user}!</b> you can review your vs other teams performance on dashboard'
                )

        response = {
            'success': 'true',
            'message': message,
            'end': request.POST['end'],
        }

        return JsonResponse(data=response, safe=False)


class QuizLiveQuestionAccessJSON(View):

    def get(self, request, quiz_id, question_id, user_id, skip):
        # TODO: please write query to avoid re-attempting quiz
        statements = []
        images = []
        audios = []
        choices_keys = []
        choices_values = []
        id = 0

        ''' __FETCHING BASE DATA__'''
        quiz = Quiz.objects.get(pk=quiz_id)
        screen = Screen.objects.get(no=user_id)
        attempts = Attempt.objects.filter(quiz=quiz, user=request.user)
        user_team = Team.objects.filter(quiz=quiz, participants=request.user)[0]

        if skip == 1:
            for user in user_team.participants.all():
                result = QuizCompleted.objects.filter(
                    user=user, quiz=quiz
                )[0]
                result.skipped += 1

                value = result.remains
                ll = value.split(',')
                ll.append(ll.pop(0))
                result.remains = ','.join(map(str, ll))
                result.save()

        # _____________________________________________________________________________________________________________
        # LOGIC: Get Remains etc.

        result = QuizCompleted.objects.filter(user=request.user, quiz=quiz)[0]
        ll = result.remains.split(',')

        # _____________________________________________________________________________________________________________
        # LOGIC: Get Questions
        # remaining = Question.objects.exclude(id__in=attempts.values_list('question', flat=True))
        # remaining = [remaining.get(pk=x) for x in questions_get]

        '''__QUESTION LOGIC WILL BE HERE__'''
        try:
            question = Question.objects.get(pk=ll[0])
            qquestion = QuizQuestion.objects.get(question=question, quiz=quiz)
        except ValueError:
            messages.success(request=request, message="Your Quiz has been submitted successfully")
            return redirect('application:quizes')

        ''' __FETCHING IMAGES AUDIOS CHOICES AND STATEMENTS__'''

        # CONTROL
        control = qquestion.submission_control.no
        submission = 0
        user_no = identify_user_in_team(user_team, request, quiz)
        if user_no == control:
            submission = 1

        # STATEMENTS
        for statement in qquestion.statementvisibility_set.all():
            if user_no == 3 and statement.screen_3:
                statements.append(statement.statement.statement)
            elif user_no == 2 and statement.screen_2:
                statements.append(statement.statement.statement)
            elif user_no == 1 and statement.screen_1:
                statements.append(statement.statement.statement)

        # CHOICES
        if submission == 1:
            for choice in qquestion.choicevisibility_set.all():
                choices_keys.append(choice.choice.pk)
                choices_values.append(choice.choice.text)
        else:
            for choice in qquestion.choicevisibility_set.all():
                if user_no == 3 and choice.screen_3:
                    choices_keys.append(choice.choice.pk)
                    choices_values.append(choice.choice.text)
                elif user_no == 2 and choice.screen_2:
                    choices_keys.append(choice.choice.pk)
                    choices_values.append(choice.choice.text)
                elif user_no == 1 and choice.screen_1:
                    choices_keys.append(choice.choice.pk)
                    choices_values.append(choice.choice.text)

        for image in qquestion.imagevisibility_set.all():
            if user_no == 3 and image.screen_3:
                var = [
                    images.append(image.image.image.url) if image.image.image else images.append(image.image.url)]
            elif user_no == 2 and image.screen_2:
                var = [
                    images.append(image.image.image.url) if image.image.image else images.append(image.image.url)]
            elif user_no == 1 and image.screen_1:
                var = [
                    images.append(image.image.image.url) if image.image.image else images.append(image.image.url)]

        for audio in qquestion.audiovisibility_set.all():
            if user_no == 3 and audio.screen_3:
                var = [
                    audios.append(audio.audio.audio.url) if audio.audio.audio else images.append(audio.audio.url)]
            elif user_no == 2 and audio.screen_2:
                var = [
                    audios.append(audio.audio.audio.url) if audio.audio.audio else audios.append(audio.audio.url)]
            elif user_no == 1 and audio.screen_1:
                var = [
                    audios.append(audio.audio.audio.url) if audio.audio.audio else audios.append(audio.audio.url)]

        # IMAGES AND AUDIOS

        total = quiz.questions.count()
        attempts = Attempt.objects.filter(user=request.user, quiz=quiz).count()
        remains = total - attempts

        ''' __GENERATING RESPONSES__'''
        response = {
            'question': question.pk,
            'submission': submission,
            'choices_keys': choices_keys,
            'choices_values': choices_values,
            'statements': statements,
            'images': images,
            'audios': audios,
            'questions': ll,

            'total': total,
            'attempts': attempts,
            'remains': remains,
        }
        return JsonResponse(data=response, safe=False)


class QuizLiveQuestionNextJSON(View):

    def post(self, request):
        success = False
        message = None
        end = False
        change = False


        quiz = Quiz.objects.get(pk=request.POST['quiz_id'])
        question = Question.objects.get(pk=request.POST['question_id'])

        quiz_complete = QuizCompleted.objects.filter(quiz=quiz, user=request.user)[0]
        question_ids = request.POST['question_ids']
        if question_ids != quiz_complete.remains:
            change = True

        if Attempt.objects.filter(user=request.user, question=question, quiz=quiz):
            success = True
        else:
            message = "Question is not submitted by you team"

        response = {
            'change': change,
            'success': success,
            'message': message,
            'end': request.POST['end']
        }

        return JsonResponse(data=response, safe=False)


class UserExistsJSON(View):

    def get(self, request, username):
        flag = False
        try:
            user = User.objects.get(username=username)
            flag = True
        except User.DoesNotExist:
            pass

        response = {
            'flag': flag
        }
        return JsonResponse(data=response, safe=False)
