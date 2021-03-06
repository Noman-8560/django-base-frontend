import json
import statistics

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import never_cache
from django.views.generic import ListView, DeleteView, UpdateView
from notifications.signals import notify

from cocognite import settings
from src.accounts.decorators import identification_required, student_required
from src.accounts.models import StudentProfile
from src.application.models import (
    Quiz, Question, QuestionChoice,
    QuizQuestion, Screen, Team, QuizCompleted,
    Attempt, LearningResourceResult, LearningResourceAttempts,
    Relation, QuizMisc,
)
from src.portals.student.bll import question_grading_logic
from src.portals.student.dll import identify_user_in_team
from src.portals.student.forms import TeamForm
from src.portals.student.helpers import generate_signature
from src.zoom_api.views import zoom_create_meeting, zoom_delete_meeting, zoom_create_user

User = get_user_model()

student_decorators = [login_required, identification_required, student_required]
student_nocache_decorators = [login_required, identification_required, student_required, never_cache]

"""  VIEWS ================================================================================= """


@method_decorator(student_decorators, name='dispatch')
class DashboardView(View):

    def get(self, request):
        allow = False

        # ALL_QUIZES
        all_quizes = Quiz.objects.filter(learning_purpose=False).order_by('-start_time')
        my_teams = Team.objects.filter(participants__in=[request.user.id])
        my_quizes = Quiz.objects.filter(id__in=my_teams.values_list('quiz', flat=True))

        total_quizzes = my_quizes.count()
        total_learning = LearningResourceResult.objects.filter(user=request.user).count()
        total_relations = Relation.objects.filter(child=request.user, is_verified_by_child=True).count()

        # AVAILABLE_QUIZES
        available_quizes = Quiz.objects.filter(
            end_time__gte=timezone.now(),
            learning_purpose=False,
            start_time__lte=timezone.now()) \
            .order_by('-start_time')

        completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id)

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
                requested_quiz = Quiz.objects.get(pk=int(request.GET.get('quiz')))

                questions = requested_quiz.questions.all()
                all_teams = Team.objects.filter(quiz=requested_quiz)

                current_team = all_teams.get(participants__in=[request.user])

                list_time_max = []
                list_time_min = []
                list_time_avg = []

                list_total_pass = []
                list_total_correct = []
                list_total_incorrect = []

                list_avg_pass = []
                list_avg_correct = []
                list_avg_incorrect = []

                list_team_pass = []
                list_team_correct = []
                list_team_incorrect = []

                list_time_my_team = []
                for question in questions:
                    _attempts = Attempt.objects.filter(quiz=requested_quiz, question=question).values('team').distinct()
                    list_time_values = []

                    _min_time = -1
                    _avg_time = 0
                    _current_team_time = 0

                    _total_correct = 0
                    _total_incorrect = 0
                    _total_pass = 0

                    _current_team_attempt = 0

                    teams_passed = [x.pk for x in all_teams]

                    for v in _attempts.values('start_time', 'end_time', 'team', 'question', 'successful'):
                        current = (v['end_time'] - v['start_time']).total_seconds()

                        list_time_values.append(current)
                        print(current)
                        print(v['team'])

                        if v['successful']:
                            _total_correct += 1
                        else:
                            _total_incorrect += 1

                        if v['team'] == current_team.pk:
                            _current_team_time = current
                            if v['successful']:
                                _current_team_attempt = 1
                            else:
                                _current_team_attempt = 0

                        if v['team'] in teams_passed:
                            teams_passed.remove(v['team'])

                    print(list_time_values)

                    try:
                        list_time_max.append(round(max(list_time_values), 2))
                    except:
                        list_time_max.append(0)

                    try:
                        list_time_min.append(round(min(list_time_values), 2))
                    except:
                        list_time_min.append(0)

                    try:
                        list_time_avg.append(round(statistics.mean(list_time_values), 2))
                    except:
                        list_time_avg.append(0)

                    list_total_pass.append(round(len(teams_passed), 2))
                    list_total_correct.append(round(_total_correct, 2))
                    list_total_incorrect.append(round(_total_incorrect, 2))
                    list_time_my_team.append(round(_current_team_time, 2))

                    list_avg_pass.append(round(len(teams_passed) / all_teams.count(), 2))
                    list_avg_correct.append(round(_total_correct / all_teams.count(), 2))
                    list_avg_incorrect.append(round(_total_incorrect / all_teams.count(), 2))

                    if current_team.pk in teams_passed:
                        list_team_pass.append(1)
                        list_team_correct.append(0)
                        list_team_incorrect.append(0)
                    else:
                        list_team_pass.append(0)
                        if _current_team_attempt == 1:
                            list_team_correct.append(1)
                            list_team_incorrect.append(0)
                        else:
                            list_team_correct.append(0)
                            list_team_incorrect.append(1)

                chart_1 = {
                    'time_max': list_time_max,
                    'time_min': list_time_min,
                    'time_avg': list_time_avg,
                    'time_my_team': list_time_my_team,
                    'questions': [x for x in range(len(questions))]
                }

                chart_2 = {
                    'total_pass': list_total_pass,
                    'total_correct': list_total_correct,
                    'total_incorrect': list_total_incorrect
                }

                chart_3 = {
                    'avg_pass': list_avg_pass,
                    'avg_correct': list_avg_correct,
                    'avg_incorrect': list_avg_incorrect
                }

                chart_4_5_6 = {
                    'avg_pass': list_avg_pass,
                    'avg_correct': list_avg_correct,
                    'avg_incorrect': list_avg_incorrect,
                    'team_pass': list_team_pass,
                    'team_correct': list_team_correct,
                    'team_incorrect': list_team_incorrect
                }

                context = {
                    'chart_1': chart_1,
                    'chart_2': chart_2,
                    'chart_3': chart_3,
                    'chart_4': chart_4_5_6,
                    'allow': allow,
                    'questions': [count + 1 for count in range(len(questions))],

                    'quizes_all': all_quizes,  # QUIZ=> REQUIRED(current, upcoming)
                    'quizes_available': available_quizes,  # QUIZ=> REQUIRED(upcoming, not_enrolled)
                    'quizes_enrolled': enrolled_quizes,
                    # QUIZ=> REQUIRED(upcoming, not_attempted) [CHECK_MODEL = QuizCompleted]
                    'quizes_completed': completed_by_me  # QUIZ=> REQUIRED(Attempted)
                }

            except Quiz.DoesNotExist:
                allow = False
                messages.error(request, 'Requested quiz does not exists.')
            except Team.DoesNotExist:
                allow = False
                messages.error(request, 'You have not participated in the requested quiz.')

        context['total_relations'] = total_relations
        context['total_quizzes'] = total_quizzes
        context['total_learning'] = total_learning

        return render(request=request, template_name='student/dashboard.html', context=context)


@method_decorator(student_decorators, name='dispatch')
class StudentProfileDetailView(UpdateView):
    template_name = 'student/studentprofile_update_form.html'
    model = StudentProfile
    fields = [
        'grade', 'school_name', 'school_email', 'parent_email', 'age'
    ]
    success_url = reverse_lazy('student-portal:profile-detail')

    def get_object(self, queryset=None):
        profile = self.request.user.get_student_profile()
        return profile

    def form_valid(self, form):
        messages.success(self.request, "Your profile updated successfully")
        return super(StudentProfileDetailView, self).form_valid(form)


@method_decorator(student_decorators, name='dispatch')
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
        enrolled_quizes = Team.objects \
            .filter(quiz__end_time__gt=timezone.now(), quiz__learning_purpose=False) \
            .exclude(quiz__id__in=completed_by_me.values_list('quiz', flat=True)).order_by('-quiz__start_time')

        # QUIZ SUBMITTED
        completed = Quiz.objects.filter(pk__in=completed_by_me.values_list('quiz', flat=True), learning_purpose=False)

        context = {
            'quizes_all': all_quizes,  # QUIZ=> REQUIRED(current, upcoming)
            'quizes_available': available_quizes,  # QUIZ=> REQUIRED(upcoming, not_enrolled)
            'quizes_enrolled': enrolled_quizes.filter(participants__in=[request.user]),
            # QUIZ=> REQUIRED(upcoming, not_attempted)[CHECK_MODEL = QuizCompleted]
            'quizes_completed': completed_by_me  # QUIZ=> REQUIRED(Attempted)
        }
        return render(request=request, template_name='student/quiz_list.html', context=context)


@method_decorator(student_decorators, name='dispatch')
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


@method_decorator(student_nocache_decorators, name='dispatch')
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
        quiz = team.quiz

        # TODO: statistics ---------------------------------------------------------
        for user in team.participants.all():
            profile = user.get_student_profile()
            if quiz.learning_purpose:
                profile.total_learning -= 1
            else:
                profile.total_quizzes -= 1
            profile.save()

        quiz.total_enrolled_teams = quiz.total_enrolled_teams + 1
        quiz.total_enrolled_students = quiz.total_enrolled_students - (
                quiz.total_enrolled_students * int(quiz.players))
        if quiz.total_enrolled_students == 0:
            quiz.total_enrolled_students = 0

        if quiz.total_enrolled_teams < 0:
            quiz.total_enrolled_teams = 0
        quiz.save()
        # --------------------------------------------------------------------------

        # TODO: Team meeting delete here
        zoom_delete_meeting(team.zoom_meeting_id)
        team.delete()
        messages.success(request=request,
                         message="Successfully unenrolled from the quiz")
        return redirect('student-portal:quiz', permanent=True)


@method_decorator(student_nocache_decorators, name='dispatch')
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

            # USER_EXISTS_OR_NOT
            try:

                if quiz.players == '2' or quiz.players == '3':

                    player_2 = User.objects.get(username=request.POST['player_2'])
                    if quiz.players == '3':
                        player_3 = User.objects.get(username=request.POST['player_3'])

                        # PLAYER_3_ASSIGNED_OR_NOT
                        if Team.objects.filter(participants__username=player_3.username, quiz=quiz).count() != 0:
                            messages.warning(
                                request=request, message=f'Requested participant or participants '
                                                         f'already enrolled choose different partners.'
                            )
                            return HttpResponseRedirect(reverse('student-portal:quiz-enroll', args=(quiz.pk,)))

                    # PLAYER_3_ASSIGNED_OR_NOT
                    if Team.objects.filter(participants__username=player_2.username, quiz=quiz).count() != 0:
                        messages.warning(request=request,
                                         message=f'Requested participant or participants '
                                                 f'already enrolled choose different partners.'
                                         )
                        return HttpResponseRedirect(reverse('student-portal:quiz-enroll', args=(quiz.pk,)))

            except User.DoesNotExist:
                messages.error(request=request, message=f'Requested participant or participants does not exists.')
                return HttpResponseRedirect(reverse('student-portal:quiz-enroll', args=(quiz.pk,)))

            #  --------- MEETING --------- #

            meeting_id = None
            start_url = None
            join_url = None

            if int(quiz.players) > 1:
                # TODO: Team meeting create here
                response = zoom_create_meeting(name=f"QUIZ {quiz.title} - TEAM {team_name}",
                                               start_time=quiz.start_time.timestamp(),
                                               end_time=quiz.end_time.timestamp(), host=request.user.email)
                if response.status_code != 201:
                    if response.status_code == 404:
                        messages.error(
                            request=request,
                            message=f'You email is not registered with Zoom - '
                                    f'Please add your zoom account in profile '
                        )
                        return HttpResponseRedirect(reverse('student-portal:profile-detail'))
                    else:
                        messages.error(
                            request=request,
                            message=f'Failed To create zoom meeting please consult administration'
                        )
                    return HttpResponseRedirect(reverse('student-portal:quiz-enroll', args=(quiz.pk,)))

                meeting = json.loads(response.text)
                meeting_id = meeting['id']
                start_url = meeting['start_url']
                join_url = meeting['join_url']

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

            # TODO: statistics ---------------------------------------------------------
            quiz.total_enrolled_teams = quiz.total_enrolled_teams + 1
            quiz.total_enrolled_students = quiz.total_enrolled_students + int(quiz.players)
            quiz.save()
            # --------------------------------------------------------------------------

            ps = [request.user.pk]
            if player_2 is not None:
                ps.append(player_2.pk)
            if player_3 is not None:
                ps.append(player_3.pk)

            for user in ps:
                _user = User.objects.get(pk=user)
                profile = _user.get_student_profile()
                if quiz.learning_purpose:
                    profile.total_learning += 1
                else:
                    profile.total_quizzes += 1
                profile.save()

                desc = f"<b>Hi {user}!</b> you have registered to take part in <b>{quiz.title}</b>, " \
                       f"scheduled on <b>{quiz.start_time.ctime()}</b>" \
                       f" your team is <b>{team.name}</b> and members are {', '.join([str(elem) for elem in ps])}."

                notify.send(
                    request.user,
                    recipient=_user,
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


@method_decorator(student_nocache_decorators, name='dispatch')
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

            completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id, passed=F('total'), quiz=user_quiz)
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

        start_url = user_team.zoom_join_url
        if user_team.created_by == request.user:
            start_url = user_team.zoom_start_url

        if user_quiz.players != '1':

            role = 0
            if user_team.created_by == request.user:
                role = 1

            data = {
                'apiKey': settings.ZOOM_API_KEY_JWT,
                'apiSecret': settings.ZOOM_API_SECRET_JWT,
                'meetingNumber': user_team.zoom_meeting_id,
                'role': role,
            }
            signature = generate_signature(data)

            context = {
                'meeting_id': user_team.zoom_meeting_id,
                'start_url': user_team.zoom_start_url,
                'created_by': user_team.created_by,
                'join_url': user_team.zoom_join_url,
                'api_key': settings.ZOOM_API_KEY_JWT,
                'api_secret': settings.ZOOM_API_SECRET_JWT,
                'signature': signature,
                'time_status': time_status,
                'allowed_to_start': allowed_to_start,
                'quiz_start_date': user_quiz.start_time,
                'quiz_end_date': user_quiz.end_time,
                'question_ids': question_ids,
                'team_id': user_team.pk,
                'quiz_id': user_quiz.pk,
                'user_no': user_no,
                'submission_control': submission,
                'quiz': Quiz.objects.get(pk=pk)
            }
        else:
            context = {
                'time_status': time_status,
                'allowed_to_start': allowed_to_start,
                'quiz_start_date': user_quiz.start_time,
                'quiz_end_date': user_quiz.end_time,
                'question_ids': question_ids,
                'team_id': user_team.pk,
                'start_url': start_url,
                'quiz_id': user_quiz.pk,
                'user_no': user_no,
                'submission_control': submission,
                'quiz': Quiz.objects.get(pk=pk)
            }

        return render(request=request, template_name='student/quiz_live_extended.html', context=context)


@method_decorator(student_decorators, name='dispatch')
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


@method_decorator(student_decorators, name='dispatch')
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


@method_decorator(student_decorators, name='dispatch')
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


@method_decorator(student_decorators, name='dispatch')
class RelationDeleteView(DeleteView):
    template_name = 'student/relation_delete.html'
    model = Relation
    success_url = reverse_lazy('student-portal:relation')

    def get_object(self, queryset=None):
        return get_object_or_404(Relation.objects.filter(child=self.request.user), pk=self.kwargs['pk'])


"""  LEARNING RESOURCE --------------------------------------------------------------------- """


@method_decorator(student_decorators, name='dispatch')
class LearningResourceListView(View):

    def get(self, request):
        # AVAILABLE_QUIZES
        available_quizes = Quiz.objects.filter(learning_purpose=True).order_by('-start_time')
        completed_by_me = LearningResourceResult.objects.filter(user__id=request.user.id).order_by('-created')

        context = {
            'available_quizes': available_quizes,
            'completed_quizes': completed_by_me,
        }
        return render(request=request, template_name='student/learning_resource_list.html', context=context)


@method_decorator(student_decorators, name='dispatch')
class LearningResourceLiveView(View):

    def get(self, request, quiz_id):
        user_quiz = None
        allowed_to_start = False
        time_status = None
        question_ids = []

        """ QUIZ and TEAM is required here """
        try:
            user_quiz = Quiz.objects.get(pk=quiz_id)
        except Quiz.DoesNotExist:
            messages.error(request=request, message="Requested Learning Resource doesn't exists")
            return redirect('student-portal:learning-resource', permanent=True)

        if not user_quiz.questions.all():
            messages.error(request=request,
                           message="Learning resource is incomplete no questions are associated with this - "
                                   "please consult admin")
            return redirect('student-portal:learning-resource', permanent=True)

        time_status = 'present'

        questions = user_quiz.questions.all()
        for question in questions:
            question_ids.append(question.pk)

        context = {
            'total': user_quiz.questions.count(),
            'time_status': time_status,
            'quiz_start_date': user_quiz.start_time,
            'quiz_end_date': user_quiz.end_time,
            'question_ids': question_ids,
            'quiz_id': user_quiz.pk,
        }

        return render(request=request, template_name='student/learning_resource_live.html', context=context)


@method_decorator(student_decorators, name='dispatch')
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


class ActivateZoomAccount(View):

    def get(self, request):

        profile = request.user.get_student_profile()
        response = zoom_create_user(request.user)

        # CREATE ZOOM USER
        if response.status_code == 201:
            messages.success(request, "Requested user zoom account created successfully-  verify to continue.")
        if response.status_code == 409:
            messages.warning(request, "Requested user zoom account already exists")

        return redirect('student-portal:profile-detail')


"""  EXTRA VIEWS ---------------------------------------------------------------------------- """


class ZoomMeetingView(View):

    def get(self, request, quiz):
        user_quiz = Quiz.objects.get(pk=quiz)
        user_team = Team.objects.filter(quiz=user_quiz, participants=request.user)[0]

        role = 0
        if user_team.created_by == request.user:
            role = 1

        data = {
            'apiKey': settings.ZOOM_API_KEY_JWT,
            'apiSecret': settings.ZOOM_API_SECRET_JWT,
            'meetingNumber': user_team.zoom_meeting_id,
            'role': role,
        }
        signature = generate_signature(data)

        context = {
            'meeting_id': user_team.zoom_meeting_id,
            'start_url': user_team.zoom_start_url,
            'created_by': user_team.created_by,
            'join_url': user_team.zoom_join_url,
            'api_key': settings.ZOOM_API_KEY_JWT,
            'api_secret': settings.ZOOM_API_SECRET_JWT,
            'signature': signature,
        }

        return render(request=request, template_name='student/zoom_meeting.html', context=context)


""" C-API =================================================================================== """


@method_decorator(student_decorators, name='dispatch')
class LearningResourceLiveQuestionSubmitJSON(View):
    def post(self, request):
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
            choice = QuestionChoice.objects.get(pk=choice_id)

            """------------------------------------------------------------"""
            """                     SAVING DATA                            """
            """------------------------------------------------------------"""

            learn_previous = LearningResourceResult.objects.filter(user=request.user, quiz=quiz)
            if len(learn_previous) == 0:
                LearningResourceAttempts(
                    question=question,
                    user=request.user,
                    quiz=quiz,
                    choice=choice,
                    start_time=request.POST['start_time'],
                    end_time=request.POST['end_time'],
                    successful=correct
                ).save()
            else:
                x = LearningResourceAttempts.objects.filter(question=question, user=request.user, quiz=quiz)[0]
                x.start_time = request.POST['start_time']
                x.end_time = request.POST['end_time']
                x.successful = correct
                x.choice = choice
                x.save()

            # TODO: QUESTION STATS > learning resource
            """ QUESTION STATS -------------------------------------------- """
            question.total_times_attempted_in_learning += 1
            if correct:
                question.total_times_correct_in_learning += 1
            question.save()
            """ ---------------------------------------------------------- """

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


@method_decorator(student_decorators, name='dispatch')
class LearningResourceLiveQuestionAccessJSON(View):

    def get(self, request, question_id, quiz_id):
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
            [images.append(None) if y.url is None else images.append(y.url) for y in
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
            print(response)
            return JsonResponse(data=response, safe=False)
        else:
            return JsonResponse(data=None, safe=False)


@method_decorator(student_decorators, name='dispatch')
class QuizLiveQuestionSubmitJSON(View):

    def post(self, request):
        success = False
        message = None
        end = False

        # VALUES FROM POST >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        quiz = Quiz.objects.get(pk=request.POST['quiz_id'])
        question = Question.objects.get(pk=request.POST['question_id'])
        team = Team.objects.get(pk=request.POST['team_id'])

        miscellaneous = QuizMisc.objects.filter(quiz=quiz, question=question, team=team)
        if not miscellaneous:
            response = {
                'success': 'false',
                'message': "No Choice has been selected by your team, "
                           "please select any choice or ask your teammates to select, if in case "
                           "any issue try to re-select it."
            }
            return JsonResponse(data=response, safe=False)

        miscellaneous = miscellaneous[0]
        # GET USERS AND ATTEMPTS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

        users = team.participants.all()
        attempt = Attempt.objects.filter(user=request.user, question=question, quiz=quiz)

        # SAVING INFO >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        for user in users:

            Attempt(
                quiz=quiz, user=user, question=question, team=team,
                start_time=request.POST['start_time'], end_time=request.POST['end_time'],
                successful=miscellaneous.choice.is_correct
            ).save()

            quiz_complete = QuizCompleted.objects.filter(quiz=quiz, user=user)[0]
            quiz_complete.passed += 1
            u = quiz_complete.remains.split(',')
            u = [int(i) for i in u]
            u.pop(0)
            u = ','.join([str(elem) for elem in u])
            quiz_complete.remains = u

            if miscellaneous.choice.is_correct:
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

        # TODO: statistics ---------------------------------------------------------
        if miscellaneous.choice.is_correct:
            question.total_times_correct_in_quizzes += 1
        question.total_times_attempted_in_quizzes += 1
        question.save()
        question_grading_logic(question)
        # ---------------------------------------------------------------------------

        miscellaneous.delete()
        response = {
            'success': 'true',
            'message': message,
            'end': request.POST['end'],
        }

        return JsonResponse(data=response, safe=False)


@method_decorator(student_decorators, name='dispatch')
class QuizLiveQuestionAccessJSON(View):

    def get(self, request, quiz_id, question_id, user_id, skip):
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

        # CONTROL >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        control = qquestion.submission_control.no
        submission = 0
        user_no = identify_user_in_team(user_team, request, quiz)
        if user_no == control:
            submission = 1

        # STATEMENTS CHOICES IMAGES AUDIOS >>>>>>>>>>>>>>>>>>>>>>>>>>>

        for statement in qquestion.statementvisibility_set.all():
            if user_no == 3 and statement.screen_3:
                statements.append(statement.statement.statement)
            elif user_no == 2 and statement.screen_2:
                statements.append(statement.statement.statement)
            elif user_no == 1 and statement.screen_1:
                statements.append(statement.statement.statement)

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

        # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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


@method_decorator(student_decorators, name='dispatch')
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


@method_decorator(student_decorators, name='dispatch')
class QuizLiveChoiceSubmitJSON(View):

    def post(self, request):

        # VALUES FROM POST
        quiz = Quiz.objects.get(pk=request.POST['quiz_id'])
        question = Question.objects.get(pk=request.POST['question_id'])
        team = Team.objects.get(pk=request.POST['team_id'])
        choice = QuestionChoice.objects.get(pk=request.POST['choice_id'])

        # CREATE TEMP RECORD
        miscellaneous = QuizMisc.objects.filter(quiz=quiz, question=question, team=team)
        if not miscellaneous:
            QuizMisc.objects.create(quiz=quiz, question=question, team=team, user=request.user, choice=choice)
        else:
            miscellaneous = miscellaneous[0]
            miscellaneous.choice = choice
            miscellaneous.user = request.user
            miscellaneous.save()

        # RESPONSE
        response = {
            'success': 'true',
            'message': 'message',
        }

        return JsonResponse(data=response, safe=False)


@method_decorator(student_decorators, name='dispatch')
class UserExistsJSON(View):

    def get(self, request, username):
        flag = False
        user = User.objects.filter(username=username, is_student=True).exclude(username=self.request.user.username)
        if user:
            flag = True

        response = {
            'flag': flag,
        }
        return JsonResponse(data=response, safe=False)
