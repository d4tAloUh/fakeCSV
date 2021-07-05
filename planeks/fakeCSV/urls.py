from django.urls import path
from .views import SchemaListView, SchemaCreateView

urlpatterns = [
    path('', SchemaListView.as_view(), name='user-schemas'),
    path('schema/', SchemaCreateView.as_view(), name='create-schema')
]
