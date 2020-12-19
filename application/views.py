import json

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import datetime

from application.BusinessLogicLayer import identify_user_in_team
from .forms import *
from .models import *


def home(request):
    articles = Article.objects.filter(active=True)
    context = {
        'articles': articles,
    }
    return render(request=request, template_name='home.html', context=context)


def article(request, pk):
    try:
        article_ = Article.objects.get(pk=pk)
        context = {
            'article': article_
        }
        return render(request=request, template_name='article.html', context=context)
    except Article.DoesNotExist:
        messages.error(request=request, message=f'Requested Article [ID: {pk}] Does not Exists.')
        return HttpResponseRedirect(reverse('application:home'))


def add_article(request, pk=0):
    if pk != 0:
        try:
            ad_check = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            messages.error(request=request, message=f'Requested Advertisement [ID: {pk}] Does not Exists.')
            return HttpResponseRedirect(reverse('application:home'))

    if request.method == 'POST':
        if pk == 0:
            form = ArticleForm(request.POST)
            if form.is_valid():
                add_form = form.save(commit=True)
                messages.success(request=request,
                                 message="Article Added Successfully - Redirected to Articles.")
                return redirect('application:home', permanent=True)
        else:
            form = ArticleForm(request.POST or None, instance=Article.objects.get(pk=pk))
            if form.is_valid():
                update_form = form.save(commit=True)
                messages.success(request=request,
                                 message=f"Article {pk} Updated Successfully - Redirected to Articles.")
                return redirect('application:home', permanent=True)
    else:
        if pk == 0:
            form = ArticleForm()
        else:
            form = ArticleForm(instance=Article.objects.get(pk=pk))

    context = {
        'form': form
    }
    return render(request=request, template_name='add_article.html', context=context)


def help_view(request):
    designing = AppUpdate.objects.filter(status='des').filter(active=True)
    designing_ = AppUpdate.objects.filter(status='des').filter(active=False)

    development = AppUpdate.objects.filter(status='dev').filter(active=True)
    development_ = AppUpdate.objects.filter(status='dev').filter(active=False)

    # testing = AppUpdate.objects.get(status='tes')

    context = {
        'designing': designing,
        'designing_': designing_,
        'development': development,
        'development_': development_,
        'testing': None,
    }
    return render(request=request, template_name='help.html', context=context)


def parent_login(request):
    return render(request=request, template_name='parents_login.html')


def profile_update(request):
    return render(request=request, template_name='profile_update.html')


def quiz_builder(request):
    return render(request=request, template_name='quiz_builder.html')


def learning_resource(request):
    quizzes = Quiz.objects.all()
    context = {'quizzes': quizzes}
    return render(request=request, template_name='learning_resource.html', context=context)


def learning_resource_quiz(request):
    id = request.GET.get('id', 0)
    print(str(id))
    quiz = Quiz.objects.get(id=id)
    context = {'quiz': quiz}
    return render(request=request, template_name='learning_resource_quiz.html', context=context)


''' QUESTION BUILDER VIEWS _______________________________________________________________'''


def question_builder(request):
    if request.method == 'POST':
        question_form_save = QuestionForm(request.POST)
        if question_form_save.is_valid():
            question = question_form_save.save(commit=True)
            messages.success(request=request,
                             message="Question Added Successfully - Redirected to Question Description.")
            return redirect('application:question_builder_update', question.pk, permanent=True)

    context = {
        'form': QuestionForm,
    }
    return render(request=request, template_name='question_builder.html', context=context)


def question_builder_update(request, pk):
    try:
        question_form = QuestionForm(request.POST or None, instance=Question.objects.get(pk=pk))
        if request.method == 'POST':
            if question_form.is_valid():
                question_form.save(commit=True)
    except:
        messages.error(request=request, message=f'Requested Question [ID: {pk}] Does not Exists.')
        return HttpResponseRedirect(reverse('application:question_builder'))

    context = {
        'question_id': pk,
        'form_question': question_form,
        'form_question_choice': QuestionChoiceForm,
        'form_question_image': QuestionImageForm,
        'form_question_audio': QuestionAudioForm,
        'form_question_statement': QuestionStatementForm,

        'data_question_statements': QuestionStatement.objects.filter(question=Question.objects.get(pk=pk)),
        'data_question_images': QuestionImage.objects.filter(question=Question.objects.get(pk=pk)),
        'data_question_audios': QuestionAudio.objects.filter(question=Question.objects.get(pk=pk)),
        'data_question_choices': QuestionChoice.objects.filter(question=Question.objects.get(pk=pk)),
    }
    return render(request=request, template_name='question_builder_update.html', context=context)


def question_statement_add(request, question):
    if request.method == 'POST':

        form = QuestionStatementForm(request.POST)
        if form.is_valid():
            question_ref = Question.objects.get(pk=question)
            statement = form.cleaned_data['statement']
            screen = form.cleaned_data['screen']

            question_statement = QuestionStatement.objects.create(
                question=question_ref, statement=statement, screen=screen
            )

            response_data = {
                "pk": question_statement.pk,
                "statement": question_statement.statement,
                "screen": question_statement.screen.name,
            }

            messages.success(request=request,
                             message="Statements added to question Successfully - Redirected to Question Description.")
            return redirect('application:question_builder_update', question, permanent=True)
            # return JsonResponse(response_data, safe=False)

    messages.error(request=request, message=f'Error in adding statement')
    return HttpResponseRedirect(reverse('application:question_builder'))


@csrf_exempt
def add_question_statement(request):
    if request.method == 'POST':
        text = request.POST['text']
        question_id = request.POST['pk']
        statement = QuestionStatement()
        statement.statement = text
        statement.question = Question.objects.get(pk=question_id)
        statement.save()
        response = {
            'statement': text
        }
        return JsonResponse(data=response, safe=False)
    else:
        return JsonResponse(data=None)


@csrf_exempt
def add_question_choice(request):
    if request.method == 'POST':
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
    else:
        return JsonResponse(data=None)


@csrf_exempt
def delete_question_choice(request, pk):
    if request.method == 'GET':
        QuestionChoice.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)
    else:
        return JsonResponse(data=None)


@csrf_exempt
def delete_question_statement(request, pk):
    if request.method == 'GET':
        QuestionStatement.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)
    else:
        return JsonResponse(data=None)


@csrf_exempt
def get_question_statements(request, pk):
    if request.method == 'GET':
        statements = QuestionStatement.objects.filter(question=Question.objects.get(pk=pk))
        serialized_queryset = serializers.serialize('python', statements)
        response = {
            'statements': serialized_queryset
        }
        return JsonResponse(data=response, safe=False)
    else:
        return JsonResponse(data=None)


def question_statement_delete(request, pk):
    try:
        question_statement = QuestionStatement.objects.get(pk=pk)
        question_id = question_statement.question.pk
        question_statement.delete()

        messages.success(request=request, message=f"Statement of Question > {question_id} deleted successfully")
        return redirect('application:question_builder_update', question_id, permanent=True)
    except:
        messages.error(request=request, message=f"Failed To Delete > Requested Statement ({pk}) Does not Exists")

    return redirect('application:question_builder', permanent=True)


def question_choices_add(request, question):
    if request.method == 'POST':

        form = QuestionChoiceForm(request.POST)
        if form.is_valid():
            question_ref = Question.objects.get(pk=question)
            text = form.cleaned_data['text']
            is_correct = form.cleaned_data['is_correct']

            question_choice = QuestionChoice.objects.create(
                text=text, is_correct=is_correct, question=question_ref
            )

            response_data = {
                "pk": question_choice.pk,
                "text": question_choice.text,
                "is_correct": question_choice.is_correct,
            }

            messages.success(
                request=request, message="choice added to question Successfully - Redirected to Question Description."
            )
            return redirect('application:question_builder_update', question, permanent=True)
            # return JsonResponse(response_data, safe=False)

    messages.error(request=request, message=f'Error in adding choices')
    return HttpResponseRedirect(reverse('application:question_builder'))


def question_choice_delete(request, pk):
    try:
        question_choice = QuestionChoice.objects.get(pk=pk)
        question_id = question_choice.question.pk
        question_choice.delete()

        messages.success(request=request, message=f"Choice of Question > {question_id} deleted successfully")
        return redirect('application:question_builder_update', question_id, permanent=True)
    except QuestionChoice.DoesNotExist:
        messages.error(request=request, message=f"Failed To Delete > Requested Choice ({pk}) Does not Exists")

    return redirect('application:question_builder', permanent=True)


def question_image_add(request, question):
    if request.method == 'POST':

        form = QuestionImageForm(request.POST, request.FILES)
        if form.is_valid():
            question_ref = Question.objects.get(pk=question)
            url = form.cleaned_data['url']
            image = form.cleaned_data['image']
            screen = form.cleaned_data['screen']

            question_image = QuestionImage.objects.create(
                url=url, image=image, screen=screen, question=question_ref
            )

        response_data = {}
        messages.success(
            request=request, message="Image attached to question Successfully - Redirected to Question Description."
        )
        return redirect('application:question_builder_update', question, permanent=True)
        # return JsonResponse(response_data, safe=False)
    messages.error(request=request, message=f'Error in adding images')
    return HttpResponseRedirect(reverse('application:question_builder'))


def question_image_delete(request, pk):
    try:
        question_image = QuestionImage.objects.get(pk=pk)
        question_id = question_image.question.pk
        question_image.delete()

        messages.success(request=request, message=f"Image of Question > {question_id} deleted successfully")
        return redirect('application:question_builder_update', question_id, permanent=True)
    except:
        messages.error(request=request, message=f"Failed To Delete > Requested Image ({pk}) Does not Exist ")

    return redirect('application:question_builder', permanent=True)


def question_audio_add(request, question):
    if request.method == 'POST':

        form = QuestionAudioForm(request.POST, request.FILES)
        if form.is_valid():
            question_ref = Question.objects.get(pk=question)
            url = form.cleaned_data['url']
            audio = form.cleaned_data['audio']
            screen = form.cleaned_data['screen']

            question_audio = QuestionAudio.objects.create(
                url=url, audio=audio, screen=screen, question=question_ref
            )

        response_data = {}
        messages.success(
            request=request, message="Audio attached to question Successfully - Redirected to Question Description."
        )
        return redirect('application:question_builder_update', question, permanent=True)
        # return JsonResponse(response_data, safe=False)
    messages.error(request=request, message=f'Error in adding audios')
    return HttpResponseRedirect(reverse('application:question_builder'))


def question_audio_delete(request, pk):
    try:
        question_audio = QuestionAudio.objects.get(pk=pk)
        question_id = question_audio.question.pk
        question_audio.delete()

        messages.success(request=request, message=f"Audio of Question > {question_id} deleted successfully")
        return redirect('application:question_builder_update', question_id, permanent=True)
    except QuestionAudio.DoesNotExist:
        messages.error(request=request, message=f"Failed To Delete > Requested audio ({pk}) Does not Exists")

    return redirect('application:question_builder', permanent=True)


''' QUIZ BUILDER VIEWS _______________________________________________________________'''


def quiz_builder(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=True)
            messages.success(request=request,
                             message="Quiz Added Successfully - Redirected to Quiz Description.")
            return redirect('application:quiz_builder_update', quiz.pk, permanent=True)
    else:
        form = QuizForm()

    context = {
        'form': form
    }
    return render(request=request, template_name='quiz_builder.html', context=context)


def search_question(request):
    search = str(request.GET['search'])
    questions_models = Question.objects.filter(questionstatement__statement__icontains=search).distinct()

    dict_out = {}
    count = 0
    for question in questions_models:
        dict = {
            'question': question.pk,
            'statement': QuestionStatement.objects.filter(question=question)[0].statement,
            'subject': question.subject.title,
            'level': 'easy',
        }
        dict_out[count] = dict
        count += 1

    dict_out['length'] = count

    return JsonResponse(dict_out, safe=False)


def quiz_builder_update(request, pk):
    question = None
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        messages.error(request=request, message=f'Requested Quiz [ID: {pk}] Does not Exists.')
        return HttpResponseRedirect(reverse('application:quiz_builder'))

    if request.method == 'POST':

        form = QuizForm(request.POST or None, instance=Quiz.objects.get(pk=pk))
        if form.is_valid():
            form.save(commit=True)
            messages.success(request=request,
                             message="Quiz Updated Successfully - You can do more see options below.")

    else:
        form = QuizForm(instance=Quiz.objects.get(pk=pk))

    context = {
        'questions': quiz.questions.all(),
        'subjects': quiz.subjects.all(),
        'quiz_id': pk,
        'total': quiz.questions.count(),
        'remaining': 00,
        'selected': 00,
        'hard': 00,
        'normal': 00,
        'easy': 00,
        'form': form,
    }
    return render(request=request, template_name='quiz_builder_update.html', context=context)


def quiz_question_add(request, quiz, question):
    quiz_model = None
    question_model = None

    try:
        quiz_model = Quiz.objects.get(pk=quiz)
        question_model = Question.objects.get(pk=question)

    except [Quiz.DoesNotExist, Question.DoesNotExist]:
        messages.error(request=request, message=f'Requested Quiz or Question Does not Exists.')
        return HttpResponseRedirect(reverse('application:quiz_builder'))

    if quiz_model.questions.filter(pk=question):
        messages.warning(request=request,
                         message=f'Failed to add > Requested Question [ID: {question}] already associated with this quiz.')
    else:
        messages.success(request=request, message=f'Requested Question [ID: {question}] added successfully.')
        quiz_model.questions.add(question_model)
        quiz_model.save()

    return redirect('application:quiz_builder_update', quiz, permanent=True)


def quiz_question_delete(request, quiz, question):
    try:
        quiz_model = Quiz.objects.get(pk=quiz)
        question_model = Question.objects.get(pk=question)

        quiz_model.questions.remove(question_model)
        messages.success(request=request, message=f'Requested Question [ID: {question}] deleted successfully.')
        return redirect('application:quiz_builder_update', quiz, permanent=True)
    except [Quiz.DoesNotExist, Question.DoesNotExist]:
        messages.error(request=request, message=f'Requested Quiz or Question Does not Exists.')
        return HttpResponseRedirect(reverse('application:quiz_builder'))


''' QUIZ SETUP VIEWS _______________________________________________________________'''


def quizes(request):
    """  ----------------------------------------------------------------------------------------------------------- """
    """
    quizes = Quiz.objects.all()
    teams = Team.objects.filter(participants__username=request.user.username)
    quizes_available = Quiz.objects.filter(~Q(teams__participants=request.user))
    quizes_enrolled = Quiz.objects.filter(teams__participants=request.user)

    print(type(n), "   ", type(Quiz.objects.filter(teams__participants__username=request.user.username)))
    print(Quiz.objects.filter(teams__participants__username=request.user.username))

    QuizCompleted.objects.filter(user=request.user)
    print(QuizCompleted.objects.filter(user=request.user))
    print(Team.objects.filter(participants__username=request.user.username))
    print(Quiz.objects.filter(teams__in=teams))
    """
    '''  ----------------------------------------------------------------------------------------------------------- '''

    # TODO : Queries need to be correct at all.
    context = {
        'quizes_all': Quiz.objects.all(),  # QUIZ=> REQUIRED(current, upcoming)
        'quizes_available': Quiz.objects.all(),  # QUIZ=> REQUIRED(upcoming, not_enrolled)
        'quizes_enrolled': Quiz.objects.all()  # QUIZ=> REQUIRED(upcoming, not_attempted)[CHECK_MODEL = QuizCompleted]
    }
    return render(request=request, template_name='quizes.html', context=context)


def teams(request):
    teams = Team.objects.filter(participants__username=request.user.username)

    context = {
        'teams': teams
    }
    return render(request=request, template_name='teams.html', context=context)


def team(request, pk):
    team = None
    try:
        team = Team.objects.get(pk=pk)

    except Team.DoesNotExist:
        messages.error(request=request, message=f'Requested Team with [ ID:{pk} ] does not exists.')
        return HttpResponseRedirect(reverse('application:teams'))

    context = {
        'team': team,
        'players': team.participants.all()
    }
    return render(request=request, template_name='team.html', context=context)


def enroll(request, pk):
    # CHECK_QUIZ_EXISTS
    quiz = None
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        messages.error(request=request, message=f'Requested Quiz with [ ID:{pk} ]does not exists.')
        return HttpResponseRedirect(reverse('application:quizes'))

    # ALREADY_ALLOCATED
    if Team.objects.filter(participants__username=request.user.username, quiz=quiz).count() != 0:
        messages.warning(request=request, message=f'You are already enrolled to this quiz')
        return HttpResponseRedirect(reverse('application:quizes'))

    # POST_METHOD
    if request.method == 'POST':
        team_name = request.POST['team_name']
        player_1 = request.user
        player_2 = None
        player_3 = None

        # USER_EXISTS_OR_NOT
        try:

            player_2 = User.objects.get(username=request.POST['player_2'])
            if quiz.players == '3':
                player_3 = User.objects.get(username=request.POST['player_3'])

                # PLAYER_3_ASSIGNED_OR_NOT
                if Team.objects.filter(participants__username=player_3.username, quiz=quiz).count() != 0:
                    messages.warning(request=request,
                                     message=f'Requested participant or participants '
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

        team = Team(name=team_name, quiz=quiz)
        team.save()

        team.participants.add(player_1, player_2, player_3)
        messages.success(request=request, message=f'You have successfully enrolled to quiz={quiz.title} '
                                                  f'with team={team_name} as a caption of team.')
        return HttpResponseRedirect(reverse('application:quizes'))

    # GET_METHOD
    context = {
        'quiz': quiz,
        'form': TeamForm()
    }
    return render(request=request, template_name='add_team.html', context=context)


def quiz_user_1(request, quiz):
    user_team = None
    user_quiz = None
    allowed_to_start = False
    time_status = None
    question_ids = []
    quiz_id = None
    user_no = None

    ''' QUIZ and TEAM is required here'''
    try:
        user_quiz = Quiz.objects.get(pk=quiz)
        user_team = Team.objects.filter(quiz=quiz, participants=request.user)[0]
        if not user_team:
            messages.error(request=request,
                           message="You are not registered to any team _ please register your team first")
            return redirect('application:quizes', permanent=True)

        if len(QuizCompleted.objects.filter(user=request.user, quiz=user_quiz)) > 0:
            messages.error(request=request, message="Dear User you have already attempted this quiz")
            return redirect('application:quizes', permanent=True)

    except Quiz.DoesNotExist:
        messages.error(request=request, message="Requested Quiz doesn't exists")
        return redirect('application:quizes', permanent=True)

    if user_quiz.start_time <= timezone.now() < user_quiz.end_time:
        allowed_to_start = True
        time_status = 'present'

        questions = user_quiz.questions.all()
        for question in questions:
            question_ids.append(question.pk)
        user_no = identify_user_in_team(user_team, request, user_quiz)

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
        'team_id': user_team.pk,
        'quiz_id': user_quiz.pk,
        'user_no': user_no
    }

    return render(request=request, template_name='quiz_user_1.html', context=context)


def quiz_user_2(request):
    return render(request=request, template_name='quiz_user_2.html')


def quiz_user_3(request):
    return render(request=request, template_name='quiz_user_3.html')


''' CAPI VIEWS _______________________________________________________________'''


def user_exists_json(request, username):
    if request.method == 'GET':
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
    else:
        return JsonResponse(data=None)


def quiz_access_question_json(request, quiz_id, question_id, user_id):
    statements = []
    images = []
    audios = []
    choices_keys = []
    choices_values = []

    if request.method == 'GET' and request.is_ajax():

        ''' __FETCHING BASE DATA__'''
        quiz = Quiz.objects.get(pk=quiz_id)
        screen = Screen.objects.get(no=user_id)

        '''__QUESTION LOGIC WILL BE HERE__'''
        question = quiz.questions.get(pk=question_id)

        '''__FETCHING SUBMISSION AND CHOICES CONTROL__'''
        submission_permitted = screen == question.submission_control
        choices_permitted = screen == question.choices_control

        ''' __FETCHING IMAGES AUDIOS CHOICES AND STATEMENTS__'''
        [statements.append(x.statement) for x in question.questionstatement_set.filter(screen=screen)]
        [images.append(y.image) if y.url is None else images.append(y.url) for y in
         question.questionimage_set.filter(screen=screen)]
        [audios.append(z.audio) if z.url is None else audios.append(z.url) for z in
         question.questionaudio_set.filter(screen=screen)]
        if choices_permitted:
            [choices_keys.append(c['pk']) for c in question.questionchoice_set.all().values('pk')]
            [choices_values.append(c['text']) for c in question.questionchoice_set.all().values('text')]

        ''' __GENERATING RESPONSES__'''
        response = {
            'permissions': {
                'submission_permitted': submission_permitted,
                'choices_permitted': choices_permitted,
            },
            'question': question.pk,
            'choices_keys': choices_keys,
            'choices_values': choices_values,
            'statements': statements,
            'images': images,
            'audios': audios
        }
        return JsonResponse(data=response, safe=False)
    else:
        return JsonResponse(data=None)


@csrf_exempt
def question_submission_json(request):
    success = False
    message = None
    end = False

    """ CHECK API CALL """
    if request.method == 'POST':

        quiz_id = request.POST['quiz_id']
        question__id = request.POST['question_id']
        team_id = request.POST['team_id']
        choice_id = request.POST['choice_id']

        users = Team.objects.get(pk=team_id).participants.all()
        attempt = Attempt.objects.filter(user=request.user, question=Question.objects.get(pk=question__id))

        """ QUIZ EXISTENCE WRT USER"""
        if len(QuizCompleted.objects.filter(user=request.user, quiz=Quiz.objects.get(pk=quiz_id))) == 0:

            """ CHECK ATTEMPTED OR NOT"""
            if len(attempt) == 0:

                """ CHECK CORRECT OR NOT """
                correct = QuestionChoice.objects.get(pk=choice_id).is_correct

                """------------------------------------------------------------"""
                """                     SAVING DATA                            """
                """------------------------------------------------------------"""

                for user in users:
                    Attempt(
                        question=Question.objects.get(pk=question__id),
                        user=user,
                        start_time=request.POST['start_time'],
                        end_time=request.POST['end_time'],
                        successful=correct
                    ).save()

                if request.POST['end'] == 'True':
                    for user in users:
                        QuizCompleted(
                            user=user,
                            quiz=Quiz.objects.get(pk=quiz_id)
                        ).save()

                success = True
                message = f"Question {request.POST['question_id']} marked successfully"

            else:
                success = False
                message = f"Question {request.POST['question_id']} already marked"
        else:
            message = f"Requested Quiz attempted previously"

        response = {
            'success': success,
            'message': message,
            'end': request.POST['end'],
        }

        return JsonResponse(data=response, safe=False)


@csrf_exempt
def next_question_json(request):
    success = False
    message = None
    end = False

    """ CHECK API CALL """
    if request.method == 'POST':

        quiz = Quiz.objects.get(pk=request.POST['quiz_id'])
        question = Question.objects.get(pk=request.POST['question_id'])

        if len(Attempt.objects.filter(user=request.user, question=question)) > 0:
            success = True
            message = "Question submitted Successfully"
        else:
            message = "Question is not submitted by you team"

        response = {
            'success': success,
            'message': message,
            'end': request.POST['end'],
        }

        return JsonResponse(data=response, safe=False)
