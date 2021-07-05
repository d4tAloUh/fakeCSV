from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView
from .models import Schema


class SchemaListView(ListView):
    model = Schema
    template_name = 'schema/index.html'
    context_object_name = 'user_schemas'

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)


class SchemaCreateView(CreateView):
    model = Schema
    template_name = 'schema/create.html'
    context_object_name = 'user_schemas'
    fields = '__all__'