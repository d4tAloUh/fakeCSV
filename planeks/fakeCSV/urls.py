from django.urls import path
from .views import SchemaListView, SchemaCreateView, SchemaUpdateView, SchemaDeleteView, DataSetListView

urlpatterns = [
    path('', SchemaListView.as_view(), name='user-schemas'),
    path('schema/create', SchemaCreateView.as_view(), name='create-schema'),
    path('schema/update/<int:pk>/', SchemaUpdateView.as_view(), name='update-schema'),
    path('schema/delete/<int:pk>/', SchemaDeleteView.as_view(), name='delete-schema'),
    path('schema/<int:pk>/datasets', DataSetListView.as_view(), name='schema-datasets'),
]
