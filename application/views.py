from django.shortcuts import render


def home(request):
    return render(request=request, template_name='home.html')


def signup(request):
    return render(request=request, template_name='signup.html')


def login(request):
    return render(request=request, template_name='login.html')


def parent_login(request):
    return render(request=request, template_name='parents_login.html')


def profile_update(request):
    return render(request=request, template_name='profile_update.html')

