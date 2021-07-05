from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView
from .models import Schema


class SchemaListView(ListView):
    model = Schema
    template_name = 'schema/index.html'

    def get_queryset(self):
        return Schema.objects.filter(user=self.request.user)
