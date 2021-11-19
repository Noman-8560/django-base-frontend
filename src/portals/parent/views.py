from django.views.generic import (
    DetailView, CreateView, ListView, DeleteView, UpdateView
)

from src.application.models import Child


class DashboardView(DetailView):
    template_name = 'parent/base.html'


class ChildListView(ListView):
    model = Child


class ChildDetailView(DetailView):
    model = Child


class ChildCreateView(CreateView):
    model = Child


class ChildUpdateView(UpdateView):
    model = Child


class ChildDeleteView(DeleteView):
    model = Child
