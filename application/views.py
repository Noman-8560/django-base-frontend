from django.shortcuts import render
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

    context = {
        'form': QuestionForm,
    }
    return render(request=request, template_name='question_builder.html', context=context)


def question_builder_update(request):

    context = {
        'form': QuestionForm,
        'form_question_choice': QuestionChoiceForm,
        'form_question_image': QuestionImageForm,
        'form_question_audio': QuestionAudioForm,
        'form_question_statement': QuestionStatementForm,
    }
    return render(request=request, template_name='question_builder_update.html', context=context)