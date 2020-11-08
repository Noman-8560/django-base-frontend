from django.shortcuts import render
from application.models import *

from application.models import *


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


def question_builder(request):
    subjects = Subject.objects.all()

    context = {
        'subjects': subjects
    }
    return render(request=request, template_name='question_builder.html', context=context)
