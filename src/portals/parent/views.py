from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView, CreateView, ListView, DeleteView, UpdateView, TemplateView
)
from django.views.generic.base import View

from src.accounts.models import User
from src.application.models import Relation, RelationType, Quiz, QuizCompleted, LearningResourceResult, Attempt, \
    LearningResourceAttempts


class DashboardView(TemplateView):
    template_name = 'parent/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        context['relations'] = Relation.objects.filter(parent=self.request.user)
        return context


class RelationListView(ListView):
    model = Relation
    template_name = 'parent/relation_list.html'

    def get_queryset(self):
        return Relation.objects.filter(parent=self.request.user, is_verified_by_child=True)

    def get_context_data(self, **kwargs):
        context = super(RelationListView, self).get_context_data(**kwargs)
        context['relation_list_unverified'] = Relation.objects.filter(
            parent=self.request.user, is_verified_by_child=False
        )
        return context


class RelationDetailView(DetailView):
    model = Relation
    template_name = 'parent/relation_create_form.html'


class RelationCreateView(View):
    template_name = 'parent/relation_create_form.html'

    def get(self, request):
        context = {'relation_types': RelationType.objects.filter(active=True).values('pk', 'guardian_relation_name')}
        return render(request, template_name=self.template_name, context=context)

    def post(self, request):
        message = "Username or Relation is Wrong"

        # if username and relation_type exists
        if request.POST['username'] and request.POST['relation_type']:
            user = User.objects.filter(username=request.POST['username'])
            relation_type = RelationType.objects.filter(pk=request.POST['relation_type'])

            # if relation type exists
            if user and relation_type:
                relation_type = relation_type[0]
                user = user[0]

                # requested account is not a student
                if user.is_student:

                    # already registered or not
                    relation = Relation.objects.filter(parent=self.request.user, child=user)
                    if not relation:
                        Relation(parent=self.request.user, child=user, relation=relation_type).save()
                        messages.success(
                            request, f"{user} is added as your {relation_type.student_relation_name} is pending"
                        )
                        return redirect('parent-portal:relation')
                    else:
                        message = f"Requested already, ask your {relation[0].relation.student_relation_name} to give accept it."
                        if relation.filter(is_verified_by_child=True):
                            message = f"{user} is already registered as your {relation[0].relation.student_relation_name}"

                else:
                    message = "Requested account is not a student"

            else:
                message = "This username is not associated with any student account"
        else:
            message = "Username or Relation is missing"

        messages.error(request, message)
        return redirect("parent-portal:relation-create")


class RelationUpdateView(UpdateView):
    model = Relation


class RelationDeleteView(DeleteView):
    template_name = 'parent/relation_delete.html'
    model = Relation
    success_url = reverse_lazy('parent-portal:relation')

    def get_object(self, queryset=None):
        return get_object_or_404(Relation.objects.filter(parent=self.request.user), pk=self.kwargs['pk'])


""" CHILDREN """


def get_child_record(context, user):
    relation = context['object']
    child = relation.child
    quizzes = QuizCompleted.objects.filter(user=child)
    learns = LearningResourceResult.objects.filter(user=child)

    """ QUIZ AND LEARN >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> """

    quizzes_passed = quizzes_failed = 0
    learns_passed = learns_failed = 0

    for quiz in quizzes:
        if quiz.obtained >= quiz.total / 2:
            quizzes_passed += 1
        else:
            quizzes_failed += 1

    for learn in learns:
        if learn.obtained >= learn.total / 2:
            learns_passed += 1
        else:
            learns_failed += 1

    """ CORE INFO  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> """

    context['quiz_total'] = quizzes.count()
    context['quiz_single'] = quizzes.filter(quiz__players='1').count()
    context['quiz_multi'] = quizzes.exclude(quiz__players='1').count()
    context['quiz_passed'] = quizzes_passed
    context['quiz_failed'] = quizzes_failed

    context['learn_total'] = learns.count()
    context['learn_passed'] = learns_passed
    context['learn_failed'] = learns_failed

    context['quizzes'] = quizzes
    context['learns'] = learns

    return context


class ChildDetailView(DetailView):
    model = Relation
    template_name = 'parent/child_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Relation.objects.filter(
            parent=self.request.user, is_verified_by_child=True
        ), pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ChildDetailView, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        return get_child_record(context, self.request.user)


class ChildQuizDetailView(DetailView):
    model = QuizCompleted
    template_name = 'parent/child_quiz_detail.html'

    def get_object(self, queryset=None):
        relation = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
        quiz_completed = get_object_or_404(QuizCompleted.objects.filter(user=relation.child), pk=self.kwargs['pk'])
        return quiz_completed

    def get_context_data(self, **kwargs):
        context = super(ChildQuizDetailView, self).get_context_data(**kwargs)
        quiz_completed = self.get_object()
        user = get_object_or_404(Relation, pk=self.kwargs['relation_id']).child
        attempts = Attempt.objects.filter(user=user, quiz=quiz_completed.quiz)

        context['object'] = quiz_completed
        context['attempts'] = attempts
        return context


class ChildLearningDetailView(DetailView):
    model = LearningResourceResult
    template_name = 'parent/child_learning_detail.html'

    def get_object(self, queryset=None):
        relation = get_object_or_404(Relation, pk=self.kwargs['relation_id'])
        learn = get_object_or_404(LearningResourceResult.objects.filter(user=relation.child), pk=self.kwargs['pk'])
        return learn

    def get_context_data(self, **kwargs):
        context = super(ChildLearningDetailView, self).get_context_data(**kwargs)
        learn = self.get_object()
        user = get_object_or_404(Relation, pk=self.kwargs['relation_id']).child
        attempts = LearningResourceAttempts.objects.filter(user=user, quiz=learn.quiz)

        context['object'] = learn
        context['attempts'] = attempts
        return context
