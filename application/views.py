from django.shortcuts import render


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


