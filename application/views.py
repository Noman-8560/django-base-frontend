from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import *
from .models import *


def home(request):
    return render(request=request, template_name='home.html')


def help_view(request):
    return render(request=request, template_name='help.html')


def signup(request):
    return render(request=request, template_name='signup.html')


def login(request):
    return render(request=request, template_name='login.html')


def parent_login(request):
    return render(request=request, template_name='parents_login.html')


def profile_update(request):
    return render(request=request, template_name='profile_update.html')


def quiz_user_1(request):
    return render(request=request, template_name='quiz_user_1.html')


def quiz_user_2(request):
    return render(request=request, template_name='quiz_user_2.html')


def quiz_user_3(request):
    return render(request=request, template_name='quiz_user_3.html')


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
