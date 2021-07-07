from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, DeleteView
from django.views.generic import ListView, CreateView, UpdateView
from .forms import SchemaForm, ColumnForm
from .models import Schema, Column, DataSet
from .helpers import update_or_create_schema, update_or_create_schema_columns, task_generate_data


class LoginRequiredRedirectMixin(LoginRequiredMixin):
    login_url = '/login/'


class SchemaListView(LoginRequiredRedirectMixin, ListView):
    template_name = 'schema/index.html'
    context_object_name = 'user_schemas'

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
        context['type_choices'] = Column.TYPE_CHOICES
        return context

    def get_success_url(self):
        return reverse('user-schemas')

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            schema = update_or_create_schema(request, None)
            update_or_create_schema_columns(request, schema)
        return HttpResponseRedirect(self.get_success_url())


class SchemaUpdateView(LoginRequiredRedirectMixin, TemplateView):
    template_name = 'schema/update.html'

    def get_context_data(self, **kwargs):
        context = super(SchemaUpdateView, self).get_context_data(**kwargs)
        context['schema'] = Schema.objects.prefetch_related('column_set').get(user=self.request.user,
                                                                              id=self.kwargs['pk'])
        context['type_choices'] = Column.TYPE_CHOICES
        return context

    def get_success_url(self):
        return reverse('user-schemas')

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            schema = update_or_create_schema(request, self.kwargs['pk'])
            update_or_create_schema_columns(request, schema)
        return HttpResponseRedirect(self.get_success_url())


class SchemaDeleteView(LoginRequiredRedirectMixin, DeleteView):
    model = Schema

    def get_success_url(self):
        return reverse('user-schemas')

    def get_object(self, queryset=None):
        return Schema.objects.get(user=self.request.user, id=self.kwargs['pk'])


class DataSetListView(LoginRequiredRedirectMixin, ListView):
    context_object_name = 'user_datasets'
    template_name = 'dataset/index.html'

    def get_queryset(self):
        return DataSet.objects.filter(schema_id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        print(request.POST)
        task = task_generate_data.delay(self.kwargs['pk'], request.POST['rows_amount'])
        return render(request, self.template_name, {"task_id": task.id})
