from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView, CreateView, ListView, DeleteView, UpdateView, TemplateView
)
from django.views.generic.base import View

from src.accounts.models import User
from src.application.models import Relation, RelationType


class DashboardView(TemplateView):
    template_name = 'parent/dashboard.html'


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
