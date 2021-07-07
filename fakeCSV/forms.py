from django.forms import ModelForm
from .models import Column, Schema


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        exclude = ['schema']


class SchemaForm(ModelForm):
    class Meta:
        model = Schema
        exclude = ['user']
