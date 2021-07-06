from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, DeleteView
from django.views.generic import ListView, CreateView, UpdateView
from .models import Schema


class SchemaListView(LoginRequiredMixin, ListView):
    model = Schema
    template_name = 'schema/index.html'
    context_object_name = 'user_schemas'
    login_url = '/login/'

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class SchemaCreateView(LoginRequiredMixin, TemplateView):
    model = Schema
    template_name = 'schema/create.html'
    context_object_name = 'user_schemas'
    login_url = '/login/'


class SchemaUpdateView(LoginRequiredMixin, TemplateView):
    model = Schema
    template_name = 'schema/update.html'
    context_object_name = 'user_schema'


class SchemaDeleteView(LoginRequiredMixin, DeleteView):
    model = Schema

    def get_success_url(self):
        return reverse('user-schemas')

    def get_object(self, queryset=None):
        return Schema.objects.get(user=self.request.user, id=self.kwargs['pk'])
