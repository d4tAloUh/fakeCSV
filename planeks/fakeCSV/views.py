from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, DeleteView
from django.views.generic import ListView, CreateView, UpdateView
from .forms import SchemaForm, ColumnForm
from .models import Schema, Column
from .helpers import update_or_create_schema, update_or_create_schema_columns


class LoginRequiredRedirectMixin(LoginRequiredMixin):
    login_url = '/login/'


class SchemaListView(LoginRequiredRedirectMixin, ListView):
    model = Schema
    template_name = 'schema/index.html'
    context_object_name = 'user_schemas'
    login_url = '/login/'

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class SchemaCreateView(LoginRequiredRedirectMixin, TemplateView):
    template_name = 'schema/create.html'

    def get_context_data(self, **kwargs):
        context = super(SchemaCreateView, self).get_context_data(**kwargs)
        context['schema'] = {
            "COLUMN_SEPARATOR_CHOICE": Schema.COLUMN_SEPARATOR_CHOICE,
            "STRING_CHARACTER_CHOICE": Schema.STRING_CHARACTER_CHOICE,
        }
        return context


class SchemaUpdateView(LoginRequiredRedirectMixin, TemplateView):
    template_name = 'schema/update.html'

    def get_context_data(self, **kwargs):
        context = super(SchemaUpdateView, self).get_context_data(**kwargs)
        context['schema'] = Schema.objects.prefetch_related('column_set').get(user=self.request.user,
                                                                              id=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('user-schemas')

    def post(self, request, *args, **kwargs):
        schema = update_or_create_schema(request, self.kwargs['pk'])
        update_or_create_schema_columns(request, schema)
        return HttpResponseRedirect(self.get_success_url())


class SchemaDeleteView(LoginRequiredRedirectMixin, DeleteView):
    model = Schema

    def get_success_url(self):
        return reverse('user-schemas')

    def get_object(self, queryset=None):
        return Schema.objects.get(user=self.request.user, id=self.kwargs['pk'])
