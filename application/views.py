from datetime import datetime
from itertools import product

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from notifications.signals import notify

from application.BusinessLogicLayer import identify_user_in_team
from .forms import *
from .models import *


def coming_soon(request):
    return render(request=request, template_name='coming_soon.html')


def page_404(request):
    return render(request=request, template_name='page_404.html')


def page_500(request):
    return render(request=request, template_name='page_500.html')


@user_passes_test(lambda u: u.is_superuser)
def site_builder(request):
    context = {}
    return render(request=request, template_name='site_builder.html', context=context)


@login_required
def dashboard(request):
    allow = False
    if request.user.is_superuser:
        return render(request=request, template_name='admin_dashboard.html')

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
            quiz = Quiz.objects.get(pk=request.GET.get('quiz'))

            if quiz in completed:
                print("COMPLETED")

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

            time_sum_of_all = []
            time_sum_of_max = []
            time_sum_of_min = []
            time_sum_of_avg = []
            time_sum_of_pas = []

            for question in questions:
                pass_attempts_all.append(1)
                average_pass_attempts_all.append(1)
                _attempts = Attempt.objects.filter(question=question).values('team').distinct()
                _s_attempts = _attempts.filter(successful=True)
                _u_attempts = _attempts.filter(successful=False)
                temp_denominator = _s_attempts.count() + _u_attempts.count()

                # GET TIMES -------------------------------------------------------------------------------------
                _all_time_sum = 0
                _min_time_sum = 0
                _max_time_sum = 0
                _avg_time_sum = 0

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
                    _max_time_sum += int(_max_time)
                    _min_time_sum += int(_min_time)

                time_sum_of_all.append(int(_all_time_sum))
                time_sum_of_max.append(int(_max_time_sum))
                time_sum_of_min.append(int(_min_time_sum))
                time_sum_of_avg.append(_all_time_sum / count)

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

                'time_sum_of_max': time_sum_of_max,
                'time_sum_of_min': time_sum_of_min,
                'time_sum_of_avg': time_sum_of_avg,

                'average_correct_attempts_all': average_correct_attempts_all,
                'average_incorrect_attempts_all': average_incorrect_attempts_all,
                'average_pass_attempts_all': average_pass_attempts_all,

                'quizes_all': all_quizes,  # QUIZ=> REQUIRED(current, upcoming)
                'quizes_available': available_quizes,  # QUIZ=> REQUIRED(upcoming, not_enrolled)
                'quizes_enrolled': enrolled_quizes,
                # QUIZ=> REQUIRED(upcoming, not_attempted)[CHECK_MODEL = QuizCompleted]
                'quizes_completed': completed_by_me  # QUIZ=> REQUIRED(Attempted)
            }
        except Quiz.DoesNotExist:
            allow = False
            messages.error(request, 'Requested quiz does not exists.')

    return render(request=request, template_name='student_dashboard.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def articles(request):
    context = {
        'articles': Article.objects.all()
    }
    return render(request=request, template_name='admin_articles.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_article(request, pk):
    try:
        article = Article.objects.get(pk=pk)
        out = article.delete()
        messages.success(request=request, message=f"Requested Article: {article.pk} deleted successfully.")
    except Article.DoesNotExist:
        messages.error(request=request, message=f"Requested Article ID: {pk} doesn't exists.")
    return HttpResponseRedirect(reverse('application:articles'))


from django.db.models import Min, Max, Avg


def help_view(request):
    return render(request=request, template_name='project.html')


@user_passes_test(lambda u: u.is_superuser)
def add_article(request, pk=0):
    if pk != 0:
        try:
            ad_check = Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            messages.error(request=request, message=f'Requested Article [ID: {pk}] Does not Exists.')
            return redirect('application:articles', permanent=True)

    if request.method == 'POST':
        if pk == 0:
            form = ArticleForm(request.POST)
            if form.is_valid():
                add_form = form.save(commit=True)
                messages.success(request=request,
                                 message="Article Added Successfully - Redirected to Articles.")
                return redirect('application:articles', permanent=True)
        else:
            form = ArticleForm(request.POST or None, instance=Article.objects.get(pk=pk))
            if form.is_valid():
                update_form = form.save(commit=True)
                messages.success(request=request,
                                 message=f"Article {pk} Updated Successfully - Redirected to Articles.")
                return redirect('application:articles', permanent=True)
    else:
        if pk == 0:
            form = ArticleForm()
        else:
            form = ArticleForm(instance=Article.objects.get(pk=pk))

    context = {
        'form': form
    }
    return render(request=request, template_name='add_article.html', context=context)


@login_required
@never_cache
def profile_update(request):
    profile = None

    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        if request.user.is_superuser:
            messages.warning(request,
                             f"You are super/root user may be your profile is not added by "
                             f"developer during your account creation, you can create by own using this "
                             f"link '{request.get_host()}/admin/application/profile/add/' or try to contact your "
                             f"developer, by the way you don't need any profile."
                             )
        else:
            messages.error(request, f"Your profile is not created yet, there may be some issue please contact admin.")
        return redirect('application:dashboard', permanent=True)

    basic_form = ProfileBasicForm(instance=request.user)
    school_form = ProfileSchoolForm(instance=profile)
    guardian_form = ProfileParentForm(instance=profile)
    image_form = ProfileImageForm(instance=profile)
    other_form = ProfileOtherForm(instance=profile)

    print(request.user.profile_set.first().profile)

    if request.method == 'POST':
        action = request.GET.get('action')
        if action == 'basic':
            pass
            basic_form = ProfileBasicForm(request.POST or None, instance=request.user)
            if basic_form.is_valid():
                basic_form.save(commit=True)
                messages.success(request, f'Your Name details updated')
        elif action == 'school':
            school_form = ProfileSchoolForm(request.POST or None, instance=profile)
            if school_form.is_valid():
                school_form.save(commit=True)
                messages.success(request, f'Your School details updated')
        elif action == 'guardian':
            guardian_form = ProfileParentForm(request.POST or None, instance=profile)
            if guardian_form.is_valid():
                guardian_form.save(commit=True)
                messages.success(request, f'Your Guardian details updated')
        elif action == 'image':
            image_form = ProfileImageForm(request.POST or None, request.FILES, instance=profile)
            if image_form.is_valid():
                image_form.save(commit=True)
                messages.success(request, f'Your Profile image updated')
        elif action == 'other':
            other_form = ProfileOtherForm(request.POST or None, request.FILES, instance=profile)
            if other_form.is_valid():
                other_form.save(commit=True)
                messages.success(request, f'Your Profile details updated')

    context = {
        'basic_form': basic_form,
        'school_form': school_form,
        'guardian_form': guardian_form,
        'image_form': image_form,
        'other_form': other_form,
    }
    return render(request=request, template_name='profile_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def quiz_builder(request):
    return render(request=request, template_name='quiz_builder.html')


''' QUESTION BUILDER VIEWS _______________________________________________________________'''


@user_passes_test(lambda u: u.is_superuser)
def questions(request):
    context = {
        'questions': Question.objects.all()
    }
    return render(request=request, template_name='questions.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def question_builder(request):
    # ADD/GET FORM
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            out = form.save(commit=True)
            messages.success(request=request,
                             message=f"Question {out.pk} added successfully.")
            return redirect('application:question_builder_update', out.pk, permanent=True)
    else:
        form = QuestionForm()

    context = {'form': form}
    return render(request=request, template_name='question_builder.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def update_question(request, pk):
    # UPDATE/ GET UPDATE FORM
    question = None
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return HttpResponseRedirect(reverse('application:question_builder'))

    if request.method == 'POST':
        form = QuestionForm(request.POST or None, instance=question)
        if form.is_valid():
            out = form.save(commit=True)
            messages.success(request=request,
                             message=f"Question {question.pk} updated successfully.")
            return redirect('application:question_builder_update', question.pk, permanent=True)
    else:
        form = QuestionForm(instance=question)
    context = {
        'form': form,
    }
    return render(request=request, template_name='question_builder.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_question(request, pk):
    try:
        question = Question.objects.get(pk=pk)
        out = question.delete()
        messages.success(request=request, message=f"Requested Question: {question.pk} deleted successfully.")
    except Subject.DoesNotExist:
        messages.error(request=request, message=f"Requested Question ID: {pk} doesn't exists.")
    return HttpResponseRedirect(reverse('application:questions'))


@user_passes_test(lambda u: u.is_superuser)
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
        'question': Question.objects.get(pk=pk),
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


@user_passes_test(lambda u: u.is_superuser)
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
@user_passes_test(lambda u: u.is_superuser)
def add_question_statement(request):
    if request.method == 'POST':
        text = request.POST['text']
        screen = request.POST['screen']
        question_id = request.POST['pk']
        statement = QuestionStatement()
        statement.statement = text
        statement.screen = Screen.objects.get(no=screen)
        statement.question = Question.objects.get(pk=question_id)
        statement.save()
        response = {
            'statement': text
        }
        return JsonResponse(data=response, safe=False)
    else:
        return JsonResponse(data=None)


@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
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
@user_passes_test(lambda u: u.is_superuser)
def delete_question_choice(request, pk):
    if request.method == 'GET':
        QuestionChoice.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)
    else:
        return JsonResponse(data=None)


@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
def delete_question_statement(request, pk):
    if request.method == 'GET':
        QuestionStatement.objects.get(pk=pk).delete()
        return JsonResponse(data={"message": "success"}, safe=False)
    else:
        return JsonResponse(data=None)


@csrf_exempt
@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
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


@user_passes_test(lambda u: u.is_superuser)
def quizzes(request):
    context = {
        'quizes': Quiz.objects.all(),

    }
    return render(request=request, template_name='quizzes.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def quiz_builder(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            out = form.save(commit=True)
            messages.success(request=request,
                             message=f"Quiz {out.title} added Successfully.")
            return redirect('application:quiz_builder_update', out.pk, permanent=True)
    else:
        form = QuizForm()

    context = {
        'form': form
    }
    return render(request=request, template_name='quiz_builder.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def quiz_builder_update(request, pk):
    quiz = None
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        messages.error(request=request, message=f'Requested Quiz [ID: {pk}] Does not Exists.')
        return HttpResponseRedirect(reverse('application:quiz_builder'))

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
    }
    return render(request=request, template_name='quiz_builder_update.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def update_quiz(request, pk):
    quiz = None
    try:
        quiz = Quiz.objects.get(pk=pk)
    except Quiz.DoesNotExist:
        messages.error(request=request, message=f'Requested Quiz [ID: {pk}] Does not Exists.')
        return HttpResponseRedirect(reverse('application:quiz_builder'))

    if request.method == 'POST':

        form = QuizForm(request.POST or None, instance=quiz)
        if form.is_valid():
            out = form.save(commit=True)
            messages.success(request=request,
                             message=f"Quiz {quiz.title} Updated Successfully.")
            return redirect('application:quiz_builder_update', quiz.pk, permanent=True)
    else:
        form = QuizForm(instance=quiz)
    context = {
        'form': form
    }

    return render(request=request, template_name='quiz_builder.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_quiz(request, pk):
    try:
        quiz = Quiz.objects.get(pk=pk)
        out = quiz.delete()
        messages.success(request=request, message=f"Requested Quiz: {quiz.title} deleted successfully.")
    except Subject.DoesNotExist:
        messages.error(request=request, message=f"Requested Quiz ID: {pk} doesn't exists.")
    return HttpResponseRedirect(reverse('application:quizzes'))


@user_passes_test(lambda u: u.is_superuser)
def search_question(request, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)

    quiz_subjects = quiz.subjects.all()

    search = str(request.GET['search'])
    questions_models = Question.objects.filter(subject__in=quiz_subjects).filter(
        questionstatement__statement__icontains=search).distinct()

    # TODO: Block already present questions
    questions_models = questions_models.filter(question_type=quiz.players)

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


@user_passes_test(lambda u: u.is_superuser)
@never_cache
def quiz_question_add(request, quiz, question):
    print("HELLO")
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


@user_passes_test(lambda u: u.is_superuser)
@never_cache
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


''' QUESTION BUILDER VIEWS _______________________________________________________________'''


@user_passes_test(lambda u: u.is_superuser)
def subjects(request):
    context = {
        'subjects': Subject.objects.all()
    }
    return render(request=request, template_name='subjects.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def update_subject(request, pk):
    subject = None
    try:
        subject = Subject.objects.get(pk=pk)
    except Subject.DoesNotExist:
        messages.error(request=request, message=f"Requested Subject ID: {pk} doesn't exists.")
        return HttpResponseRedirect(reverse('application:subjects'))

    if request.method == 'GET':
        form = SubjectForm(instance=subject)
    else:
        form = SubjectForm(request.POST or None, instance=subject)
        if form.is_valid():
            out = form.save(commit=True)
            messages.success(request=request,
                             message=f"Subject {out} Updated Successfully.")

    context = {'form': form}
    return render(request=request, template_name='add_subject.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def add_subject(request):
    if request.method == 'GET':
        form = SubjectForm()
    else:
        form = SubjectForm(request.POST or None)
        if form.is_valid():
            out = form.save(commit=True)
            messages.success(request=request, message=f"Subject: {out} added successfully.")
    context = {
        'form': form
    }
    return render(request=request, template_name='add_subject.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def delete_subject(request, pk):
    try:
        subject = Subject.objects.get(pk=pk)
        out = subject.delete()
        messages.success(request=request, message=f"Requested Subject: {subject.title} deleted successfully.")
    except Subject.DoesNotExist:
        messages.error(request=request, message=f"Requested Subject ID: {pk} doesn't exists.")
    return HttpResponseRedirect(reverse('application:subjects'))


''' QUIZ SETUP VIEWS _______________________________________________________________'''

from django.db.models import F


@login_required
def quizes(request):
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
    return render(request=request, template_name='quizes.html', context=context)


@login_required
def teams(request):
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
    return render(request=request, template_name='teams.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def admin_teams(request):
    context = {'teams': Team.objects.all()}
    return render(request=request, template_name='admin_teams.html', context=context)


@user_passes_test(lambda u: u.is_superuser)
def admin_team_delete(request, pk):
    try:
        team = Team.objects.get(pk=pk)
        out = team.delete()
        messages.success(request=request, message=f"Requested Team: {team.name} deleted successfully.")
    except Subject.DoesNotExist:
        messages.error(request=request, message=f"Requested Team ID: {pk} doesn't exists.")
    return HttpResponseRedirect(reverse('application:admin_teams'))


@login_required
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


@login_required
@never_cache
def delete_team(request, pk):
    team = None
    try:
        Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        messages.error(request=request, message="Requested Team Does not exists")
        return redirect('application:teams', permanent=True)

    if len(Team.objects.filter(participants__username=request.user.username, pk=pk)) == 0:
        messages.error(request=request, message="You are not allowed to delete this team")
        return redirect('application:teams', permanent=True)

    completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id)
    completed = Quiz.objects.filter(pk__in=completed_by_me.values_list('quiz', flat=True))

    if Team.objects.filter(quiz__in=completed):
        messages.error(request=request,
                       message="you have attempted quiz with this team you are not allowed to delete this team ")
        return redirect('application:teams', permanent=True)

    messages.success(request=request,
                     message="You have been removed from team")
    return redirect('application:teams', permanent=True)


@login_required
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

            if quiz.players == '2':
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

        ps = [request.user.username]

        if player_2 is not None:
            ps.append(player_2.username)

        if player_3 is not None:
            ps.append(player_3.username)

        for user in ps:
            desc = f"<b>Hi {user}!</b> you have registered to take part in <b>{quiz.title}</b>, scheduled on <b>{quiz.start_time.ctime()}</b>" \
                   f" your team is <b>{team.name}</b> and members are {', '.join([str(elem) for elem in ps])}."

            notify.send(
                request.user,
                recipient=User.objects.get(username=user),
                verb=f'Enrolled to {quiz.title}',
                level='success',
                description=desc
            )

        return HttpResponseRedirect(reverse('application:quizes'))

    # GET_METHOD
    context = {
        'quiz': quiz,
        'form': TeamForm()
    }
    return render(request=request, template_name='add_team.html', context=context)


@login_required
@never_cache
def quiz_start(request, quiz):
    user_team = None
    user_quiz = None
    allowed_to_start = False
    time_status = None
    question_ids = []
    quiz_id = None
    user_no = None
    submission = None
    new = False

    ''' QUIZ and TEAM is required here'''

    try:
        user_quiz = Quiz.objects.get(pk=quiz)
        questions = user_quiz.questions.all()
        user_team = Team.objects.filter(quiz=quiz, participants=request.user)[0]
        if not user_team:
            messages.error(request=request,
                           message="You are not registered to any team _ please register your team first")
            return redirect('application:quizes', permanent=True)

        completed_by_me = QuizCompleted.objects.filter(user__id=request.user.id, passed=F('total'))
        if completed_by_me:
            messages.error(request=request, message="Dear User you have already attempted this quiz")
            return redirect('application:quizes', permanent=True)

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

        attempts = Attempt.objects.filter(quiz=user_quiz, user=request.user)

        remaining = questions.exclude(id__in=attempts.values_list('question', flat=True))
        for re in remaining:
            question_ids.append(re.pk)
        user_no = identify_user_in_team(user_team, request, user_quiz)

        no_notify = False

        if not QuizCompleted.objects.filter(user=request.user, quiz=quiz):
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

        if user_no == user_quiz.submission_control.no:
            submission = '1'
        else:
            submission = '0'

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
        'user_no': user_no,
        'submission_control': submission,
        'quiz': Quiz.objects.get(pk=quiz)
    }

    return render(request=request, template_name='quiz_user_1.html', context=context)


@login_required
def results(request):
    # quiz = Quiz.objects.get(pk=1)
    # attempts = LearningResourceAttempts.objects.filter(quiz=quiz, user=request.user)
    # result = LearningResourceResult(quiz=quiz, user=request.user)
    #
    # print(result)
    # print(attempts)
    # print(quiz)

    return render(request=request, template_name='results.html')


@login_required
def learning_resources_result(request, quiz):
    quiz_ = None
    result = None

    try:
        quiz_ = Quiz.objects.get(pk=quiz)
        result = LearningResourceResult.objects.get(user=request.user, quiz=quiz_)
    except LearningResourceResult.DoesNotExist:
        pass
    except Quiz.DoesNotExist:
        pass

    attempts = LearningResourceAttempts.objects.filter(user=request.user, quiz=quiz_)

    context = {
        'quiz': quiz_,
        'result': result,
        'attempts': attempts
    }
    return render(request=request, template_name='learning_quiz_result.html', context=context)


@login_required
def learning_resources(request):
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
    return render(request=request, template_name='learning_resources.html', context=context)


''' CAPI VIEWS _______________________________________________________________'''


@login_required
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


@login_required
def quiz_access_question_json(request, quiz_id, question_id, user_id, skip):
    # TODO: please write query to avoid re-attempting quiz
    statements = []
    images = []
    audios = []
    choices_keys = []
    choices_values = []
    id = 0

    if request.method == 'GET' and request.is_ajax():

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
        except ValueError:
            messages.success(request=request, message="Your Quiz has been submitted successfully")
            return redirect('application:quizes')
        ''' __FETCHING IMAGES AUDIOS CHOICES AND STATEMENTS__'''
        [statements.append(x.statement) for x in question.questionstatement_set.filter(screen=screen)]
        [images.append(y.image.url) if y.url is None else images.append(y.url) for y in
         question.questionimage_set.filter(screen=screen)]
        [audios.append(z.audio.url) if z.url is None else audios.append(z.url) for z in
         question.questionaudio_set.filter(screen=screen)]
        [choices_keys.append(c['pk']) for c in question.questionchoice_set.all().values('pk')]
        [choices_values.append(c['text']) for c in question.questionchoice_set.all().values('text')]

        total = quiz.questions.count()
        attempts = Attempt.objects.filter(user=request.user, quiz=quiz).count()
        remains = total - attempts

        ''' __GENERATING RESPONSES__'''
        response = {
            'question': question.pk,
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

    else:
        return JsonResponse(data=None, safe=False)


@csrf_exempt
@login_required
def question_submission_json(request):
    success = False
    message = None
    end = False

    """ CHECK API CALL """
    if request.method == 'POST':

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

                notify.send(
                    request.user,
                    recipient=request.user,
                    verb=f'Quiz {quiz.title} submitted',
                    level='info',
                    description=f'<b>Hi {request.username}!</b> you can review your vs other teams performance on dashboard'
                )

        response = {
            'success': 'true',
            'message': message,
            'end': request.POST['end'],
        }

        return JsonResponse(data=response, safe=False)


@csrf_exempt
@login_required
def next_question_json(request):
    success = False
    message = None
    end = False
    change = False

    """ CHECK API CALL """
    if request.method == 'POST':

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


@never_cache
def learning_resources_start(request, quiz):
    user_quiz = None
    allowed_to_start = False
    time_status = None
    question_ids = []
    quiz_id = None

    ''' QUIZ and TEAM is required here'''
    try:
        user_quiz = Quiz.objects.get(pk=quiz)

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

    return render(request=request, template_name='learning_quiz.html', context=context)


@login_required
def learn_access_question_json(request, quiz_id, question_id):
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


@csrf_exempt
@login_required
def learn_question_submission_json(request):
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


# def statistics(request):
#     return JsonResponse(context)


@user_passes_test(lambda u: u.is_superuser)
def sent_mail(request):
    # send_mail(
    #     subject='Checking MAil !!',
    #     message='',
    #     from_email='donald.duck0762@gmail.com',
    #     recipient_list=['ikram.khan0762@gmail.com'],
    #     fail_silently=False,
    #     html_message='<h1><strong>HII</strong> man how are you<h2/>'
    # )
    pass
