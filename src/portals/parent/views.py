from django.contrib import messages
from django.shortcuts import render, redirect
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
            if relation_type and relation_type:
                relation_type = relation_type[0]
                user = user[0]

                # user record already added
                if not Relation.objects.filter(is_active=True, parent=self.request.user, child=user, relation=relation_type):
                    Relation(parent=self.request.user, child=user, relation=relation_type).save()
                    messages.success(
                        request, "Your relation request added successfully, "
                                 "please ask your child to give permissions to access data."
                    )
                    return redirect('parent-portal:relation')
                else:
                    message = "Relation already taken"
            else:
                message = "Relation Type Doesn't Exists."
        else:
            messages.error(request, "Username or Relation Type is wrong")
        context = {
            'relation_types': RelationType.objects.filter(active=True).values('pk', 'guardian_relation_name')
        }
        return render(request, template_name=self.template_name, context=context)


class RelationUpdateView(UpdateView):
    model = Relation


class RelationDeleteView(DeleteView):
    model = Relation
