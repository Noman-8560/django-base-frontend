from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import (
    TemplateView, ListView, DeleteView, DetailView, UpdateView, CreateView
)

from src.application.models import (
    Article, Subject, Profile, Quiz, Question, QuestionStatement, QuestionChoice, QuestionImage, QuestionAudio,
    QuizQuestion, ChoiceVisibility, ImageVisibility, StatementVisibility, AudioVisibility, Screen,
)

student_decorators = [login_required]


"""  VIEWS ======================================================================== """


"""  ARTICLES --------------------------------------------------------------------- """


"""  SUBJECTS --------------------------------------------------------------------- """


""" QUESTION ---------------------------------------------------------------------- """


""" C-API ========================================================================= """


""" CHANGE ======================================================================== """
