from django.urls import path
from .views import SchemaListView

urlpatterns = [
    path('', SchemaListView.as_view(), name='user-schemas')
]
